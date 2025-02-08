# app.py
import streamlit as st
from ahp_calculation import AHPCalculator

def main():
    st.title(" Farmer Credit Score Assessment System")

    # U1: Family Background
    st.subheader("Family Background (U1)")

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
        u1_q2_score = 2
    elif u1_q2 == "3 laborers (Good labor capacity)":
        u1_q2_score = 3
    else:
        u1_q2_score = 4

    # Identity
    u1_q3 = st.radio("What is your level of identity proof?",
                    ["No formal identity (e.g., unregistered land)", 
                    "Partial identity proof (e.g., land in dispute)", 
                    "Fully verified identity (Clear ownership or official recognition)"],
                    index=0)
    if u1_q3 == "No formal identity (e.g., unregistered land)":
        u1_q3_score = 1
    elif u1_q3 == "Partial identity proof (e.g., land in dispute)":
        u1_q3_score = 2
    else:
        u1_q3_score = 3

    # Marital Status
    u1_q4 = st.radio("What is your marital status?",
                    ["Single, unstable family support",
                    "Married, no children, moderate family support",
                    "Married with children (Stable household)"],
                    index=0)
    if u1_q4 == "Single, unstable family support":
        u1_q4_score = 1
    elif u1_q4 == "Married, no children, moderate family support":
        u1_q4_score = 2
    else:
        u1_q4_score = 3

    # Lifestyle
    u1_q5 = st.radio("What is your lifestyle?",
                    ["High-expense lifestyle (Luxury purchases or debt)",
                    "Moderate expenses (Basic needs with occasional discretionary spending)", 
                    "Simple lifestyle (Savings-oriented, minimal discretionary spending)"],
                    index=0)
    if u1_q5 == "High-expense lifestyle (Luxury purchases or debt)":
        u1_q5_score = 1
    elif u1_q5 == "Moderate expenses (Basic needs with occasional discretionary spending)":
        u1_q5_score = 2
    else:
        u1_q5_score = 3

    # Family Members' Health Condition
    u1_q6 = st.radio("What is the health condition of your family members?",
                    ["Poor health (Chronic illness in key members)",
                    "Average health (Occasional medical expenses)",
                    "Excellent health (Minimal medical risks)"],
                    index=0)
    if u1_q6 == "Poor health (Chronic illness in key members)":
        u1_q6_score = 1
    elif u1_q6 == "Average health (Occasional medical expenses)":
        u1_q6_score = 2
    else:
        u1_q6_score = 3

    # Mastery of Skills
    u1_q7 = st.radio("What is your level of skills and training?",
                    ["No skills (Untrained, low productivity)",
                    "Semi-skilled (Basic training or informal experience)",
                    "Skilled (Certified training or proven track record)"],
                    index=0)
    if u1_q7 == "No skills (Untrained, low productivity)":
        u1_q7_score = 1
    elif u1_q7 == "Semi-skilled (Basic training or informal experience)":
        u1_q7_score = 2
    else:
        u1_q7_score = 3

    # U2 Willingness to Repay
    st.subheader("Willingness to Repay (U2)")
    u2_options = [
        "I have never defaulted on a loan repayment.",
        "I have defaulted on a loan, but it was resolved.",
        "I have defaulted on a loan, and the issue remains unresolved."
    ]
    u2_q1 = st.radio("Loan Repayment History", u2_options, index=0)

    if u2_q1 == "I have never defaulted on a loan repayment.":
        u2_q1_score = 4
        u2_q2_score = 0
        u2_q3_score = 0
    elif u2_q1 == "I have defaulted on a loan, but it was resolved.":
        u2_q1_score = 2
        u2_q2_score = 2
        u2_q3_score = 0
    else:
        u2_q1_score = 1
        u2_q2_score = 0
        u2_q3_score = 1

    # U3 Ability to Repay
    st.subheader("Ability to Repay (U3)")
    u3_options = [
        "My family's average monthly income per household member is below the poverty line.",
        "My family's average monthly income per household member is enough to meet basic needs.",
        "My family's average monthly income per household member is enough to meet basic needs and save occasionally.",
        "My family's average monthly income per household member is well above the basic needs with regular savings."
    ]
    u3_q1 = st.radio("Income Level", u3_options, index=0)

    if u3_q1 == "My family's average monthly income per household member is below the poverty line.":
        u3_q1_score, u3_q2_score, u3_q3_score, u3_q4_score = 1, 0, 0, 0
    elif u3_q1 == "My family's average monthly income per household member is enough to meet basic needs.":
        u3_q1_score, u3_q2_score, u3_q3_score, u3_q4_score = 0, 2, 0, 0
    elif u3_q1 == "My family's average monthly income per household member is enough to meet basic needs and save occasionally.":
        u3_q1_score, u3_q2_score, u3_q3_score, u3_q4_score = 0, 0, 3, 0
    else:
        u3_q1_score, u3_q2_score, u3_q3_score, u3_q4_score = 0, 0, 0, 4

    # U4 Relationship with the Cooperative
    st.subheader("Relationship with the Cooperative (U4)")
    u4_options = [
        "I am not a member of any professional association.",
        "I am a member but rarely participate in activities.",
        "I am a member and participate occasionally in activities.",
        "I am an active member and regularly participate in activities."
    ]
    u4_q1 = st.radio("Cooperative Membership and Participation", u4_options, index=0)

    if u4_q1 == "I am not a member of any professional association.":
        u4_q1_score, u4_q2_score, u4_q3_score, u4_q4_score = 1, 0, 0, 0
    elif u4_q1 == "I am a member but rarely participate in activities.":
        u4_q1_score, u4_q2_score, u4_q3_score, u4_q4_score = 0, 2, 0, 0
    elif u4_q1 == "I am a member and participate occasionally in activities.":
        u4_q1_score, u4_q2_score, u4_q3_score, u4_q4_score = 0, 0, 3, 0
    else:
        u4_q1_score, u4_q2_score, u4_q3_score, u4_q4_score = 0, 0, 0, 4

    # Calculate total credit score
    ahp_calculator = AHPCalculator()
    scores = {
        'U1A1': u1_q1_score, 'U1A2': u1_q2_score, 'U1A3': u1_q3_score, 'U1A4': u1_q4_score,
        'U1A5': u1_q5_score, 'U1A6': u1_q6_score, 'U1A7': u1_q7_score,
        'U2B1': u2_q1_score, 'U2B2': u2_q2_score, 'U2B3': u2_q3_score,
        'U3C1': u3_q1_score, 'U3C2': u3_q2_score, 'U3C3': u3_q3_score, 'U3C4': u3_q4_score,
        'U4D1': u4_q1_score, 'U4D2': u4_q2_score, 'U4D3': u4_q3_score
    }

    if st.button("Submit"):
        result = ahp_calculator.check_eligibility(scores)
        if result['score'] is not None:
            if result['eligible']:
                st.write("You are eligible for the loan.")
            else:
                st.write("You are not eligible for the loan.")
            st.write(f"Total Credit Score: {result['score']:.2f}%")
        else:
            st.write(result['message'])
            st.write("Consistency Summary:")
            for line in result['consistency_summary']:
                st.write(line)

if __name__ == "__main__":
    main()