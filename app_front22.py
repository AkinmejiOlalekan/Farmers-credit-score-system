import streamlit as st
from ahp_calculation import AHPCalculator

def main():
    st.title("Farmer Credit Score Assessment System")

    # U1: Family Background
    st.subheader("Family Background")

    # Age
    # Modified to use radio buttons with ranges
    u1_q1 = st.radio("What is your age range?", [
        "Below 20 years old",
        "20-25 years old",
        "25-35 years old",
        "35-50 years old",
        "Above 60 years old"
    ], index=3)

    if u1_q1 == "Below 20 years old" or u1_q1 == "Above 60 years old":
        u1_q1_score = 1
    elif u1_q1 == "20-25 years old":
        u1_q1_score = 2
    elif u1_q1 == "25-35 years old":
        u1_q1_score = 4
    elif u1_q1 == "35-50 years old":
        u1_q1_score = 3
    else:  # 50-60 years old
        u1_q1_score = 2

    # Number of Laborers
    u1_q2 = st.radio("How many individuals in your household are engaged in labor or work-related activities?", 
                    ["0-1", 
                    "2",
                    "3",
                    "4"], 
                    index=0)
    if u1_q2 == "0-1 laborers (Insufficient labor capacity)":
        u1_q2_score = 1
    elif u1_q2 == "2 laborers (Marginally sufficient labor)":
        u1_q2_score = 3
    elif u1_q2 == "3 laborers (Good labor capacity)":
        u1_q2_score = 4
    else:
        u1_q2_score = 5

    # Identity
    u1_q3 = st.radio("What is the status of your property verification?",
                    ["No formal documentation (e.g., unregistered land)", 
                    "Partial documentation (e.g., land ownership in dispute)", 
                    "Fully verified documentation (e.g., clear ownership or official recognition)"],
                    index=0)
    if u1_q3 == "No formal documentation (e.g., unregistered land)":
        u1_q3_score = 1
    elif u1_q3 == "Partial documentation (e.g., land ownership in dispute)":
        u1_q3_score = 3
    else:
        u1_q3_score = 5

    # Marital Status
    u1_q4 = st.radio("What is your current marital and family support status?",
                    ["Single",
                    "Married",
                    "Married with children"],
                    index=0)
    if u1_q4 == "Single":
        u1_q4_score = 1
    elif u1_q4 == "Married":
        u1_q4_score = 3
    else:
        u1_q4_score = 5

    # Lifestyle
    u1_q5 = st.radio("Which best describes your approach to personal finances?",
                    ["Flexible spending (Frequent discretionary purchases or managing financial commitments)",
                    "Balanced spending (Covers essentials with occasional discretionary expenses)", 
                    "Savings-focused (Prioritizes savings with minimal discretionary spending)"],
                    index=0)
    if u1_q5 == "Flexible spending (Frequent discretionary purchases or managing financial commitments)":
        u1_q5_score = 1
    elif u1_q5 == "Balanced spending (Covers essentials with occasional discretionary expenses)":
        u1_q5_score = 3
    else:
        u1_q5_score = 5

    # Family Members' Health Condition
    u1_q6 = st.radio("How family members are facing health issues?",
                    ["1",
                    "2",
                    "3 and above"],
                    index=0)
    if u1_q6 == "1":
        u1_q6_score = 5
    elif u1_q6 == "2":
        u1_q6_score = 3
    else:
        u1_q6_score = 1

    # Mastery of Skills
    u1_q7 = st.radio("What's your years of experience as a farmer?",
                    ["0-5 years",
                    "5-10 years",
                    "10 years above"],
                    index=0)
    if u1_q7 == "0-5 years":
        u1_q7_score = 1
    elif u1_q7 == "5-10 years":
        u1_q7_score = 3
    else:
        u1_q7_score = 5

    # U2 Willingness to Repay
    st.subheader("Willingess to Repay")
    u2_options = [
        "Consistent repayment (Never defaulted on a loan)",
        "Previous default, but resolved (Loan default occurred but was settled)",
        "Outstanding default (Loan default occurred and is yet to be resolved)"
    ]
    u2_q1 = st.radio("What best describes your loan repayment history?", u2_options, index=0)

    if u2_q1 == "Consistent repayment (Never defaulted on a loan)":
        u2_q1_score = 5
        u2_q2_score = 5
        u2_q3_score = 5
        u2_q4_score = 5
    elif u2_q1 == "Previous default, but resolved (Loan default occurred but was settled)":
        u2_q1_score = 3
        u2_q2_score = 3
        u2_q3_score = 3
        u2_q4_score = 3
    else:
        u2_q1_score = 1
        u2_q2_score = 1
        u2_q3_score = 1
        u2_q4_score = 1

    # U3 Ability to Repay
    st.subheader("Ability to Repay")
    u3_options = [
        "Limited income (Covers some basic needs)",
        "Stable income (Covers basic needs)",
        "Moderate financial flexibility (Covers basic needs with occasional savings)",
        "Comfortable financial position (Exceeds basic needs with regular savings)"
    ]
    u3_q1 = st.radio("How would you describe your household’s financial capacity?", u3_options, index=0)

    if u3_q1 == "Limited income (Covers some basic needs)":
        u3_q1_score = u3_q2_score = u3_q3_score = u3_q4_score = u3_q5_score = u3_q6_score = u3_q7_score = 1
    elif u3_q1 == "Stable income (Covers basic needs)":
        u3_q1_score = u3_q2_score = u3_q3_score = u3_q4_score = u3_q5_score = u3_q6_score = u3_q7_score = 3
    elif u3_q1 == "Moderate financial flexibility (Covers basic needs with occasional savings)":
        u3_q1_score = u3_q2_score = u3_q3_score = u3_q4_score = u3_q5_score = u3_q6_score = u3_q7_score = 4
    else:
        u3_q1_score = u3_q2_score = u3_q3_score = u3_q4_score = u3_q5_score = u3_q6_score = u3_q7_score = 5

    # U4 Relationship with the Cooperative
    st.subheader("Relationship with the Cooperative")
    u4_options = [
        "Not a member of any professional or cooperative association",
        "Member with limited participation (Rarely involved in activities)",
        "Moderately engaged member (Occasionally participates in activities)",
        "Active member (Regularly participates in activities)"
    ]
    u4_q1 = st.radio("What best describes your involvement in a professional or cooperative association?", u4_options, index=0)

    if u4_q1 == "Not a member of any professional or cooperative association":
        u4_q1_score = u4_q2_score = u4_q3_score = 1
    elif u4_q1 == "Member with limited participation (Rarely involved in activities)":
        u4_q1_score = u4_q2_score = u4_q3_score = 3
    elif u4_q1 == "Moderately engaged member (Occasionally participates in activities)":
        u4_q1_score = u4_q2_score = u4_q3_score = 4
    else:
        u4_q1_score = u4_q2_score = u4_q3_score = 5

    # Calculate total credit score
    ahp_calculator = AHPCalculator()
    scores = {
        'U1A1': u1_q1_score, 'U1A2': u1_q2_score, 'U1A3': u1_q3_score, 'U1A4': u1_q4_score,
        'U1A5': u1_q5_score, 'U1A6': u1_q6_score, 'U1A7': u1_q7_score,
        'U2B1': u2_q1_score, 'U2B2': u2_q2_score, 'U2B3': u2_q3_score, 'U2B4': u2_q4_score,
        'U3C1': u3_q1_score, 'U3C2': u3_q2_score, 'U3C3': u3_q3_score, 'U3C4': u3_q4_score,
        'U3C5': u3_q5_score, 'U3C6': u3_q6_score, 'U3C7': u3_q7_score,
        'U4D1': u4_q1_score, 'U4D2': u4_q2_score, 'U4D3': u4_q3_score
    }

    if st.button("Submit"):
        result = ahp_calculator.check_eligibility(scores)
        if result['score'] is not None:
            if result['eligible']:
                st.success("You are eligible for the loan! 🎉")
            else:
                st.error("You are not eligible for the loan.")
            st.write(f"Total Credit Score: {result['score']:.2f}%")
        else:
            st.write(result['message'])
            st.write("Consistency Summary:")
            for line in result['consistency_summary']:
                st.write(line)

if __name__ == "__main__":
    main()