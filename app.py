"""
Streamlit interface for AHP-based Credit Scoring System

This script provides a web interface for the Analytic Hierarchy Process (AHP)
implementation using Streamlit. It allows users to:
1. Input main criteria and sub-criteria
2. Perform pairwise comparisons
3. Input scores for each criterion
4. Calculate final credit scores and determine loan qualification

The interface handles user input validation and provides immediate feedback
on the consistency of pairwise comparisons.
"""

import streamlit as st
import numpy as np
import pandas as pd
from ahp_core import (
    normalize_matrix, 
    consistency_check, 
    calculate_final_score,
    calculate_standardized_score
)

def create_criteria_matrix(criteria_names: list, prefix: str) -> np.ndarray:
    """
    Create and populate a pairwise comparison matrix through the Streamlit interface.
    
    Args:
        criteria_names (list): List of criterion names
        prefix (str): Prefix for Streamlit widget keys
        
    Returns:
        np.ndarray: Populated pairwise comparison matrix
    """
    n = len(criteria_names)
    matrix = np.ones((n, n))
    
    for i in range(n):
        for j in range(i + 1, n):
            value = st.number_input(
                f"How important is {criteria_names[i]} compared to {criteria_names[j]}?",
                min_value=0.1,
                max_value=09.0,
                value=1.0,
                step=0.1,
                key=f"{prefix}_{i}_{j}"
            )
            matrix[i, j] = value
            matrix[j, i] = 1 / value
    
    return matrix

def display_matrix_analysis(
    matrix: np.ndarray,
    criteria_names: list,
    section_name: str
):
    """
    Display the normalized matrix, weights, and consistency analysis.
    
    Args:
        matrix (np.ndarray): Pairwise comparison matrix
        criteria_names (list): List of criterion names
        section_name (str): Name of the section for display purposes
    """
    normalized_matrix, weights = normalize_matrix(matrix)
    
    st.subheader(f"Normalized {section_name} Matrix")
    st.dataframe(pd.DataFrame(
        normalized_matrix,
        columns=criteria_names,
        index=criteria_names
    ))
    
    st.subheader(f"{section_name} Weights")
    st.write(pd.Series(weights, index=criteria_names))
    
    # Perform consistency check
    lambda_max, CI, CR = consistency_check(matrix, weights)
    st.subheader("Consistency Check")
    st.write(f"λ_max: {lambda_max:.4f}, CI: {CI:.4f}, CR: {CR:.4f}")
    
    if CR < 0.1:
        st.success("The pairwise comparisons are consistent!")
    else:
        st.warning("The pairwise comparisons are inconsistent. Please review your inputs.")
    
    return weights

def display_final_scores(Z: float, H: float):
    """
    Display the final scores and loan qualification status.
    
    Args:
        Z (float): Total credit score
        H (float): Standardized percentage score
    """
    st.subheader("Final Scores")
    st.write(f"Total Credit Score (Z): {Z:.2f}")
    st.write(f"Standardized Percentage Score (H): {H:.2f}%")
    
    # Add loan qualification message
    if H > 70:
        st.success("This individual is qualified for the loan!")
    else:
        st.warning("This individual does not meet the minimum qualification score of 70%")

def main():
    """Main application function that sets up the Streamlit interface."""
    st.title("Credit Scoring System using AHP")
    st.write("A tool to calculate credit scores using the Analytic Hierarchy Process.")
    st.markdown("""
        - **U1** = Family background
        - **U2** = Willingness to repay  
        - **U3** = Ability to repay  
        - **U4** = Relationship
        """)

    # Step 1: Main Criteria Input
    main_criteria = st.text_input(
        "Enter main criteria (comma-separated):",
        "U1,U2,U3,U4",
    ).split(",")
    
    if len(main_criteria) > 1:
        st.subheader("Pairwise Comparison for Main Criteria")
        main_matrix = create_criteria_matrix(main_criteria, "main")
        main_weights = display_matrix_analysis(
            main_matrix,
            main_criteria,
            "Main Criteria"
        )
        
        # Step 2: Sub-Criteria and Score Calculation
        total_weighted_scores = 0
        total_weights = 0
        
        for criterion in main_criteria:
            if st.checkbox(f"Define sub-criteria for {criterion}"):
                sub_criteria = st.text_input(
                    f"Enter sub-criteria for {criterion} (comma-separated):",
                    key=f"sub_{criterion}"
                ).split(",")
                
                sub_matrix = create_criteria_matrix(sub_criteria, f"sub_{criterion}")
                sub_weights = display_matrix_analysis(
                    sub_matrix,
                    sub_criteria,
                    f"Sub-Criteria for {criterion}"
                )
                
                # Collect scores for sub-criteria
                scores = []
                for sub in sub_criteria:
                    score = st.number_input(
                        f"Enter the score for {sub} (1 to 5):",
                        min_value=1.0,
                        max_value=5.0,
                        value=3.0,
                        step=0.1,
                        key=f"score_{criterion}_{sub}"
                    )
                    scores.append(score)
                
                # Calculate scores for this criterion
                criterion_score = calculate_final_score(
                    sub_criteria,
                    sub_weights,
                    scores
                )
                main_weight = main_weights[main_criteria.index(criterion)]
                total_weighted_scores += criterion_score * main_weight
                total_weights += sum(sub_weights) * main_weight * 5
        
        # Display final scores if we have any weights
        if total_weights > 0:
            Z, H = calculate_standardized_score(total_weighted_scores, total_weights)
            display_final_scores(Z, H)

if __name__ == "__main__":
    main()