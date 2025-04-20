import google.generativeai as genai

# Configure Gemini with your API key
genai.configure(api_key="AIzaSyAYVGom4bzdvtl6iHqO_3uMsNcUpjuyFLM")  # Replace with your actual Gemini API key

# Load the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_why_explanation(predicted_algo, soft_metrics):
    prompt = f"""
    Based on the following soft metrics for CPU scheduling algorithms, explain why {predicted_algo} was chosen as the best algorithm:

    {str(soft_metrics)}

    Provide a detailed, beginner-friendly explanation that justifies why {predicted_algo} performed better than the others. A 10-12 lines paragraph
    will be good containing some bulleted points will also be good. Just start the explanation directly.Also in between explain the soft-metric terminologies that what are their meanings and then other things
    and u always have to support the predicted algo that i'm passing.
    """

    try:
        response = model.generate_content(prompt)
        ai_explanation = response.text.strip()

        # Basic validation of AI output
        if ai_explanation and len(ai_explanation.split()) > 5:
            return ai_explanation
    except Exception as e:
        print("Gemini explanation failed:", e)

    # Fallback to rule-based explanation if AI response fails
    return rule_based_explanation(predicted_algo, soft_metrics)


def rule_based_explanation(predicted_algo, soft_metrics):
    """
    Generate a fallback explanation based on predefined rules.

    Args:
        predicted_algo (str): The predicted best algorithm (e.g., 'SJF', 'FCFS')
        soft_metrics (dict): Dictionary containing metrics for each algorithm.

    Returns:
        str: Rule-based explanation of the selected algorithm.
    """
    m = soft_metrics[predicted_algo]
    reasons = []

    if m['avg_tat'] == min(val['avg_tat'] for val in soft_metrics.values()):
        reasons.append("it had the lowest average turnaround time")

    if m['avg_wt'] == min(val['avg_wt'] for val in soft_metrics.values()):
        reasons.append("it minimized average waiting time")

    if m['avg_rt'] == min(val['avg_rt'] for val in soft_metrics.values()):
        reasons.append("it had the shortest average response time")

    if m['starved'] == 0:
        reasons.append("it ensured no process starvation")

    if m['priority_violations'] == 0:
        reasons.append("it respected all priority rules")

    if m['fairness'] == min(val['fairness'] for val in soft_metrics.values()):
        reasons.append("it maintained the best fairness index")

    if not reasons:
        reasons.append("its overall performance was the most balanced")

    return f"{predicted_algo} was selected because " + ", and ".join(reasons) + "."




soft_metrics = {
    "FCFS": {"avg_tat": 29.0, "avg_wt": 5.67, "avg_rt": 5.67, "starved": 1, "fairness": 13, "priority_violations": 1},
    "SJF": {"avg_tat": 29.0, "avg_wt": 5.67, "avg_rt": 5.67, "starved": 1, "fairness": 13, "priority_violations": 1},
    "RR": {"avg_tat": 30.67, "avg_wt": 7.33, "avg_rt": 4.0, "starved": 0, "fairness": 13, "priority_violations": 2},
    "Priority": {"avg_tat": 44.0, "avg_wt": 20.67, "avg_rt": 20.67, "starved": 1, "fairness": 59, "priority_violations": 1}
}

predicted_algo = "SJF"
explanation = generate_why_explanation(predicted_algo, soft_metrics)
print("\nGenerated Explanation:\n", explanation)
