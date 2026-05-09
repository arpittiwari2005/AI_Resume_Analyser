from services.nlp_service import extract_missing_skills

jd_text = "Looking for someone to build a good, modern digital application using React and AWS."
resume_text = "I have built applications before but not with AWS."

missing = extract_missing_skills(resume_text, jd_text)
print("Missing skills detected:", missing)

# Ensure "git" (from digital), "go" (from good), "ui" (from build) are NOT in missing skills.
# Ensure "react" and "aws" ARE in missing skills since JD has them and resume doesn't have React.
# Wait, resume has "AWS", but in lowercase "aws" matching it should be picked up. Lets check.
