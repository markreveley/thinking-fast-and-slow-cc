"""
Evolutionary Selector
Scores and selects the best candidate from multiple agent outputs.
"""

from typing import List, Dict, Any, Optional, Tuple
import json


class EvolutionarySelector:
    """
    Implements evolutionary selection logic for choosing the best
    candidate solution from multiple agent outputs.
    """

    def __init__(self):
        self.scoring_criteria = {
            'completeness': 0.25,
            'correctness': 0.30,
            'clarity': 0.20,
            'feasibility': 0.15,
            'creativity': 0.10
        }

    def score_candidate(self, candidate: Dict[str, Any],
                       task: str,
                       criteria_weights: Optional[Dict[str, float]] = None) -> float:
        """
        Score a single candidate based on multiple criteria.

        Args:
            candidate: The candidate solution with metadata
            task: Original task description
            criteria_weights: Optional custom weights for scoring criteria

        Returns:
            Final weighted score (0-100)
        """
        weights = criteria_weights or self.scoring_criteria

        # Extract scores from candidate metadata
        scores = candidate.get('scores', {})

        # Calculate weighted average
        total_score = 0.0
        total_weight = 0.0

        for criterion, weight in weights.items():
            if criterion in scores:
                total_score += scores[criterion] * weight
                total_weight += weight

        # Normalize if not all criteria present
        # Note: scores are already 0-100, so no need to multiply by 100
        if total_weight > 0:
            final_score = total_score / total_weight
        else:
            # Fallback to simple rating if no detailed scores
            final_score = candidate.get('rating', 50.0)

        return final_score

    def select_best(self, candidates: List[Dict[str, Any]],
                   task: str,
                   criteria_weights: Optional[Dict[str, float]] = None) -> Tuple[Dict[str, Any], str]:
        """
        Select the best candidate from a list using evolutionary selection.

        Args:
            candidates: List of candidate solutions
            task: Original task description
            criteria_weights: Optional custom weights

        Returns:
            Tuple of (best_candidate, selection_rationale)
        """
        if not candidates:
            raise ValueError("No candidates to select from")

        if len(candidates) == 1:
            return candidates[0], "Only one candidate available"

        # Score all candidates
        scored_candidates = []
        for candidate in candidates:
            score = self.score_candidate(candidate, task, criteria_weights)
            candidate['final_score'] = score
            scored_candidates.append(candidate)

        # Sort by score (highest first)
        scored_candidates.sort(key=lambda x: x['final_score'], reverse=True)

        # Select winner
        winner = scored_candidates[0]

        # Generate rationale
        rationale = self._generate_rationale(winner, scored_candidates, task)

        return winner, rationale

    def _generate_rationale(self, winner: Dict[str, Any],
                          all_candidates: List[Dict[str, Any]],
                          task: str) -> str:
        """Generate a human-readable explanation for the selection."""

        winner_score = winner['final_score']
        runner_up_score = all_candidates[1]['final_score'] if len(all_candidates) > 1 else 0

        rationale = f"""
Selected candidate from {winner.get('agent', 'unknown')} with score {winner_score:.2f}/100.

Key strengths:
"""
        # Add top scoring criteria
        scores = winner.get('scores', {})
        if scores:
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            for criterion, score in sorted_scores[:3]:
                rationale += f"- {criterion.capitalize()}: {score:.2f}/100\n"

        if len(all_candidates) > 1:
            margin = winner_score - runner_up_score
            rationale += f"\nMargin over runner-up: {margin:.2f} points"

        rationale += f"\n\nTotal candidates evaluated: {len(all_candidates)}"

        return rationale.strip()

    def compare_two(self, candidate_a: Dict[str, Any],
                   candidate_b: Dict[str, Any],
                   task: str) -> str:
        """
        Compare two candidates and return which is better.

        Returns:
            'A', 'B', or 'TIE'
        """
        score_a = self.score_candidate(candidate_a, task)
        score_b = self.score_candidate(candidate_b, task)

        threshold = 2.0  # Minimum difference to avoid tie

        if abs(score_a - score_b) < threshold:
            return 'TIE'
        elif score_a > score_b:
            return 'A'
        else:
            return 'B'

    def rank_all(self, candidates: List[Dict[str, Any]],
                task: str) -> List[Dict[str, Any]]:
        """
        Rank all candidates by score.

        Returns:
            List of candidates sorted by score (highest first)
        """
        scored = []
        for candidate in candidates:
            score = self.score_candidate(candidate, task)
            candidate['final_score'] = score
            scored.append(candidate)

        scored.sort(key=lambda x: x['final_score'], reverse=True)
        return scored


def create_candidate(agent_name: str,
                    output: str,
                    scores: Optional[Dict[str, float]] = None,
                    confidence: float = 0.5,
                    metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Helper function to create a properly formatted candidate.

    Args:
        agent_name: Name of the agent that generated this
        output: The actual solution/response
        scores: Dictionary of criterion -> score (0-100)
        confidence: Agent's confidence in this solution (0-1)
        metadata: Any additional metadata

    Returns:
        Formatted candidate dictionary
    """
    candidate = {
        'agent': agent_name,
        'output': output,
        'confidence': confidence,
        'scores': scores or {},
        'metadata': metadata or {}
    }

    return candidate


if __name__ == "__main__":
    # Quick test
    selector = EvolutionarySelector()

    # Create test candidates
    c1 = create_candidate(
        "s1_pattern_agent",
        "Quick solution A",
        scores={'completeness': 70, 'correctness': 80, 'clarity': 85, 'feasibility': 75, 'creativity': 60},
        confidence=0.7
    )

    c2 = create_candidate(
        "s2_reasoner",
        "Detailed solution B",
        scores={'completeness': 90, 'correctness': 95, 'clarity': 88, 'feasibility': 85, 'creativity': 70},
        confidence=0.9
    )

    winner, rationale = selector.select_best([c1, c2], "Test task")
    print(f"Winner: {winner['agent']}")
    print(f"Score: {winner['final_score']:.2f}")
    print(f"\nRationale:\n{rationale}")
