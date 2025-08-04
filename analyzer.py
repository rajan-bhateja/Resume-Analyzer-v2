from crewai import Agent, Task, Crew, Process
from crewai_tools import RagTool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from dashboard import uploaded_resume

# load the environment variables
load_dotenv()

# custom RAG tool configurations
rag_config = {
    "llm": {
        "provider": "google",
        "config": {
            "model": "gemini-2.5-flash",
        }
    },
    "embedding_model": {
        "provider": "google",
        "config": {
            "model": "gemini-embedding-001"
        }
    },
    "vectordb": {
        "provider": "chroma",
        "config": {
            "collection_name": "my-collection",
        }
    },
    "chunker": {
        "chunk_size": 10,
        "chunk_overlap": 2,
        "length_function": "len",
        "min_chunk_size": 0
    }
}

pdf_rag_tool = RagTool(config=rag_config, summarize=True)
# pdf_rag_tool.add(uploaded_resume)

# LLM
groq_llm = ChatGroq(model="groq/deepseek-r1-distill-llama-70b")


# Agents
resume_analyst = Agent(
    role="Resume Content Analyzer",
    goal="Understand and summarize candidate resumes",
    backstory="You're an HR assistant trained to deeply analyze resumes, capturing key highlights and overall tone.",
    tools=[pdf_rag_tool],
    llm=groq_llm,
    verbose=True
)

skill_evaluator = Agent(
    role="Skill Assessor",
    goal="Extract and rank relevant skills from resumes",
    backstory="With expertise in parsing qualifications, you can objectively evaluate skills and assign rankings.",
    llm=groq_llm,
    verbose=True
)

job_matcher = Agent(
    role="Job Recommendation Specialist",
    goal="Suggest relevant job titles or roles based on profile",
    backstory="You're trained on job market data and adept at matching talent with opportunities.",
    llm=groq_llm,
    verbose=True
)

candidate_summarizer = Agent(
    role="Final Resume Report Generator",
    goal="Deliver a professional, insightful resume analysis",
    backstory="You're an editorial assistant that transform structured analysis into digestible executive summaries.",
    llm=groq_llm,
    verbose=True
)

# Tasks
summarize_resume = Task(
    description="Read the full resume and generate a concise summary (2–3 paragraphs) that captures the candidate’s background, key roles, education, and strengths.",
    expected_output="A 2-3 paragraph professional summary.",
    agent=resume_analyst
)

skill_extraction_and_evaluation = Task(
    description="Extract all technical and soft skills from the resume and rank them out of 100 based on how frequently and prominently they are mentioned.",
    expected_output="A list of skills with scores and a rationale.",
    agent=skill_evaluator
)

job_matching = Task(
    description="Based on the candidate's experience, skills, and education, recommend 3-5 job roles or titles they are well-suited for.",
    expected_output="A short list of job suggestions with reasoning.",
    agent=job_matcher
)

final_candidate_summary = Task(
    description="Using insights from prior agents (summary, skills, and job recommendations), generate a final report assessing the candidate's overall strength and fit in the job market.",
    expected_output="A cohesive candidate report combining all previous results in a markdown format.",
    output_file="final_summary.md",
    agent=candidate_summarizer
)

resume_analysis_crew = Crew(
    agents=[resume_analyst, skill_evaluator, job_matcher, candidate_summarizer],
    tasks=[summarize_resume, skill_extraction_and_evaluation, job_matching, final_candidate_summary],
    process=Process.sequential,
    verbose=True
)

resume_analysis_crew.kickoff()