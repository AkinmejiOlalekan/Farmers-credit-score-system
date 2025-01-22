"""
Core functionality for Analytic Hierarchy Process (AHP) calculations

This module provides the essential mathematical operations and logic required for
implementing the Analytic Hierarchy Process, a structured technique for organizing
and analyzing complex decisions.

The module includes functions for:
- Matrix normalization
- Consistency checking
- Score calculations
- Weight computations
"""

import numpy as np
from typing import Any, Tuple, List, Dict, Union

def normalize_matrix(matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Normalize a pairwise comparison matrix and calculate criteria weights.
    
    The function performs the following steps:
    1. Calculates the sum of each column
    2. Divides each element by its column sum (normalization)
    3. Calculates the average of each row to get criteria weights
    
    Args:
        matrix (np.ndarray): Square matrix of pairwise comparisons
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: 
            - Normalized matrix
            - Array of weights for each criterion
    """
    # Calculate column sums and normalize
    column_sums = matrix.sum(axis=0)
    normalized_matrix = matrix / column_sums
    
    # Calculate weights as row averages
    weights = normalized_matrix.mean(axis=1)
    return normalized_matrix, weights

def consistency_check(
    matrix: np.ndarray, 
    weights: np.ndarray
) -> Tuple[float, float, float]:
    """
    Calculate consistency metrics for the pairwise comparison matrix.
    
    Implements Saaty's method for checking consistency:
    - Calculates λmax (principal eigenvalue)
    - Computes Consistency Index (CI)
    - Determines Consistency Ratio (CR)
    
    Args:
        matrix (np.ndarray): Original pairwise comparison matrix
        weights (np.ndarray): Calculated weights for criteria
        
    Returns:
        Tuple[float, float, float]:
            - λmax: Principal eigenvalue
            - CI: Consistency Index
            - CR: Consistency Ratio
    """
    n = matrix.shape[0]
    
    # Calculate λmax
    weighted_sum_vector = np.dot(matrix, weights)
    lambda_max = np.mean(weighted_sum_vector / weights)
    
    # Calculate Consistency Index (CI)
    CI = (lambda_max - n) / (n - 1)
    
    # Random Index values for different matrix sizes (from Saaty's research)
    RI_values = {
        1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12,
        6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45
    }
    RI = RI_values.get(n, 1.45)  # Default to 1.45 for n > 9
    
    # Calculate Consistency Ratio (CR)
    CR = CI / RI if RI else 0
    
    return lambda_max, CI, CR

def calculate_final_score(
    criteria: List[str], 
    weights: np.ndarray, 
    scores: List[float]
) -> float:
    """
    Calculate the final weighted score for a set of criteria.
    
    Args:
        criteria (List[str]): List of criterion names
        weights (np.ndarray): Array of weights for each criterion
        scores (List[float]): List of scores for each criterion
        
    Returns:
        float: Final weighted score
    """
    return sum(weight * score for weight, score in zip(weights, scores))

def calculate_standardized_score(
    weighted_scores: float, 
    total_weights: float
) -> Tuple[float, float]:
    """
    Calculate standardized percentage score from weighted scores.
    
    Args:
        weighted_scores (float): Sum of all weighted scores
        total_weights (float): Sum of all weights multiplied by maximum possible score
        
    Returns:
        Tuple[float, float]:
            - Z: Total credit score
            - H: Standardized percentage score
    """
    Z = weighted_scores
    H = (Z / total_weights) * 100 if total_weights > 0 else 0
    return Z, H