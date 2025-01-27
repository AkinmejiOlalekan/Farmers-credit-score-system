# ahp_calculator.py
import numpy as np
import logging

class AHPCalculator:
    def __init__(self):
        # Random Index values for n = 1 to 10
        self.RI = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 
                   6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        
        # Initialize pairwise comparison matrices
        self.U1_matrix = np.array([
            [1, 3, 5, 7, 2, 4, 6],  # Example priorities for A1 vs others
            [1/3, 1, 3, 5, 2, 3, 4],
            [1/5, 1/3, 1, 3, 1, 2, 3],
            [1/7, 1/5, 1/3, 1, 1/2, 1, 2],
            [1/2, 1/2, 1, 2, 1, 2, 3],
            [1/4, 1/3, 1/2, 1, 1/2, 1, 2],
            [1/6, 1/4, 1/3, 1/2, 1/3, 1/2, 1]
        ])

        self.U2_matrix = np.array([
            [1, 4, 7, 5],  # Example priorities for B1 vs others
            [1/4, 1, 3, 2],
            [1/7, 1/3, 1, 1/2],
            [1/5, 1/2, 2, 1]
        ])

        self.U3_matrix = np.array([
            [1, 3, 5, 7, 4, 6, 8],  # Example priorities for C1 vs others
            [1/3, 1, 3, 5, 3, 4, 6],
            [1/5, 1/3, 1, 3, 2, 3, 4],
            [1/7, 1/5, 1/3, 1, 1/2, 2, 3],
            [1/4, 1/3, 1/2, 2, 1, 3, 4],
            [1/6, 1/4, 1/3, 1/2, 1/3, 1, 2],
            [1/8, 1/6, 1/4, 1/3, 1/4, 1/2, 1]
        ])

        self.U4_matrix = np.array([
            [1, 2, 4],  # Example priorities for D1 vs others
            [1/2, 1, 3],
            [1/4, 1/3, 1]
        ])

        
        
        # Main criteria weights
        self.main_weights = {
            'U1': 0.0954,
            'U2': 0.1601,
            'U3': 0.2772,
            'U4': 0.4673
        }

        # Validate consistency of all matrices
        self.consistency_results = self._check_all_matrices()

        # Calculate weights only if matrices are consistent
        self.weights = self._calculate_all_weights()

        # Print weights keys during initialization for debugging
        print("Weights keys:", list(self.weights.keys()) if self.weights is not None else "Weights is None")

         # Configure logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        # Validate and log consistency of matrices
        self.consistency_results = self._check_all_matrices()
        self.logger.debug("Consistency Results: %s", self.consistency_results)
        print("Consistency Results:", self.consistency_results)
        print("Are all matrices consistent?", 
          all(result['is_consistent'] for result in self.consistency_results.values()))

    def calculate_consistency(self, matrix, weights):
        """Calculate Consistency Ratio (CR) for a given matrix"""
        n = len(matrix)
        
        # Calculate weighted sum vector
        weighted_sum = np.dot(matrix, weights)
        
        # Calculate lambda max
        lambda_max = np.mean(weighted_sum / weights)
        
        # Calculate Consistency Index (CI)
        CI = (lambda_max - n) / (n - 1)
        
        # Get Random Index (RI)
        RI = self.RI.get(n, 1.49)  # Use 1.49 for n > 10
        
        # Calculate Consistency Ratio (CR)
        CR = CI / RI if RI != 0 else 0
        
        return {
            'lambda_max': lambda_max,
            'CI': CI,
            'RI': RI,
            'CR': CR,
            'is_consistent': CR < 0.1
        }

    def _check_all_matrices(self):
        """Check consistency for all matrices"""
        results = {}
        
        # Check U1 matrix
        u1_weights = self.normalize_matrix(self.U1_matrix)
        results['U1'] = self.calculate_consistency(self.U1_matrix, u1_weights)
        
        # Check U2 matrix
        u2_weights = self.normalize_matrix(self.U2_matrix)
        results['U2'] = self.calculate_consistency(self.U2_matrix, u2_weights)
        
        # Check U3 matrix
        u3_weights = self.normalize_matrix(self.U3_matrix)
        results['U3'] = self.calculate_consistency(self.U3_matrix, u3_weights)
        
        # Check U4 matrix
        u4_weights = self.normalize_matrix(self.U4_matrix)
        results['U4'] = self.calculate_consistency(self.U4_matrix, u4_weights)
        
        return results


    def normalize_matrix(self, matrix):
        """Normalize the pairwise comparison matrix and calculate weights"""
        col_sums = matrix.sum(axis=0)
        norm_matrix = matrix / col_sums
        weights = norm_matrix.mean(axis=1)
        return weights

    def _calculate_all_weights(self):
        """Calculate normalized weights for all criteria if matrices are consistent"""
        weights = {}
        
        # Check if all matrices are consistent
        all_consistent = all(result['is_consistent'] 
                        for result in self.consistency_results.values())
        
        if not all_consistent:
            return None
            
        # U1 weights
        u1_weights = self.normalize_matrix(self.U1_matrix)
        for i, w in enumerate(u1_weights):
            weights[f'U1A{i+1}'] = w
            
        # U2 weights
        u2_weights = self.normalize_matrix(self.U2_matrix)
        for i, w in enumerate(u2_weights):
            weights[f'U2B{i+1}'] = w
            
        # U3 weights
        u3_weights = self.normalize_matrix(self.U3_matrix)
        for i, w in enumerate(u3_weights):
            weights[f'U3C{i+1}'] = w
            
        # U4 weights
        u4_weights = self.normalize_matrix(self.U4_matrix)
        u4_options = ['U4D1', 'U4D2', 'U4D3']
        for i, w in enumerate(u4_weights):
            weights[u4_options[i]] = w
        
        return weights

    def get_consistency_summary(self):
        """Get a summary of consistency check results"""
        summary = []
        for category, result in self.consistency_results.items():
            status = "CONSISTENT" if result['is_consistent'] else "INCONSISTENT"
            summary.append(f"{category} Matrix: {status} (CR = {result['CR']:.3f})")
        return summary

    def calculate_score(self, scores):
        """Calculate final credit score if matrices are consistent"""
        try:
            if self.weights is None:
                self.logger.error("Weights are None")
                return None
            
            # Validate input scores
            missing_keys = set(scores.keys()) - set(self.weights.keys())
            if missing_keys:
                self.logger.error(f"Missing keys in weights: {missing_keys}")
                return None

            total_score = 0
            max_possible_score = 0
            
            for criterion, score in scores.items():
                try:
                    main_category = criterion[:2]
                    weight = self.weights[criterion] * self.main_weights[main_category]
                    total_score += score * weight
                    max_possible_score += 5 * weight
                except KeyError as e:
                    self.logger.error(f"Key error for criterion {criterion}: {e}")
                    return None
            
            percentage_score = (total_score / max_possible_score) * 100
            return percentage_score
        
        except Exception as e:
            self.logger.error(f"Unexpected error in calculate_score: {e}")
            return None
        
    def check_eligibility(self, scores):
        """Check if farmer is eligible for loan"""
        if self.weights is None:
            consistency_summary = self.get_consistency_summary()
            return {
                'score': None,
                'eligible': False,
                'message': 'Cannot calculate score: Inconsistent matrices',
                'consistency_summary': consistency_summary
            }
        
        final_score = self.calculate_score(scores)
        if final_score is None:
            return {
                'score': None,
                'eligible': False,
                'message': 'Score calculation failed',
                'consistency_summary': self.get_consistency_summary()
            }
        
        is_eligible = final_score >= 70
        return {
            'score': final_score,
            'eligible': is_eligible,
            'message': 'Eligible for loan' if is_eligible else 'Not eligible for loan',
            'consistency_summary': self.get_consistency_summary()
        }