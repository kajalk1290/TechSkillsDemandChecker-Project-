"""
Tech Skills Demand Checker
---------------------------
Yeh script job listings scrape karke Python skills ki demand check karta hai
Author: Your Name
Date: February 2026
"""

import requests
from bs4 import BeautifulSoup
from collections import Counter
import time
import re

# ====================
# STEP 1: Skills List Setup
# ====================
# Yeh woh skills hain jo hum search karenge
SKILLS_TO_TRACK = [
    'Python', 'Django', 'Flask', 'FastAPI',
    'Pandas', 'NumPy', 'Machine Learning', 'ML',
    'Data Science', 'AI', 'Artificial Intelligence',
    'SQL', 'PostgreSQL', 'MySQL', 'MongoDB',
    'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
    'Git', 'REST API', 'GraphQL',
    'TensorFlow', 'PyTorch', 'Scikit-learn',
    'Selenium', 'BeautifulSoup', 'Scrapy',
    'Jupyter', 'Data Analysis', 'ETL',
    'Linux', 'CI/CD', 'Agile', 'Scrum'
]


class TechSkillsScraper:
    """
    Main scraper class jo job listings se skills extract karta hai
    """
    
    def __init__(self):
        """Initialize the scraper with headers and storage"""
        # Headers add karte hain taaki website humein bot na samjhe
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.all_skills_found = []  # Yahan saari skills store hongi
        self.job_titles = []  # Job titles store karne ke liye
    
    def scrape_indeed_jobs(self, search_query="Python Developer", location="India", num_pages=3):
        """
        Indeed se jobs scrape karta hai
        
        Parameters:
        - search_query: Kis type ki job search karni hai
        - location: Kahan ki jobs chahiye
        - num_pages: Kitne pages scrape karne hain
        """
        print(f"\n🔍 Searching for '{search_query}' jobs in {location}...\n")
        
        for page in range(num_pages):
            try:
                # Indeed ka URL banana
                start = page * 10
                url = f"https://in.indeed.com/jobs?q={search_query.replace(' ', '+')}&l={location}&start={start}"
                
                print(f"📄 Scraping page {page + 1}...")
                
                # Website se data fetch karna
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    # HTML parse karna BeautifulSoup se
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Job cards dhundna
                    job_cards = soup.find_all('div', class_='job_seen_beacon')
                    
                    if not job_cards:
                        # Agar job cards nahi mile, alternative structure try karo
                        job_cards = soup.find_all('td', class_='resultContent')
                    
                    print(f"   ✓ Found {len(job_cards)} job listings")
                    
                    # Har job card process karna
                    for job in job_cards:
                        # Job title extract karna
                        title_elem = job.find('h2', class_='jobTitle')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            self.job_titles.append(title)
                        
                        # Job description se skills extract karna
                        desc_elem = job.find('div', class_='job-snippet')
                        if desc_elem:
                            description = desc_elem.get_text()
                            self.extract_skills(description)
                    
                    # Polite scraping: thoda wait karo next request se pehle
                    time.sleep(2)
                else:
                    print(f"   ⚠ Error: Status code {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error on page {page + 1}: {str(e)}")
                continue
    
    def scrape_github_jobs(self):
        """
        GitHub Jobs alternative - demo data use karenge
        Real GitHub Jobs band ho gaya hai, so yeh example ke liye hai
        """
        # Demo job descriptions for testing
        demo_jobs = [
            {
                'title': 'Senior Python Developer',
                'description': 'Looking for Python developer with Django, PostgreSQL, Docker, and AWS experience. Knowledge of Machine Learning is a plus.'
            },
            {
                'title': 'Data Scientist',
                'description': 'Expert in Python, Pandas, NumPy, Scikit-learn, and TensorFlow. SQL and data visualization required.'
            },
            {
                'title': 'Backend Developer',
                'description': 'Strong Python skills, Flask or FastAPI, REST API development, MongoDB, Docker, Kubernetes.'
            },
            {
                'title': 'ML Engineer',
                'description': 'Python, PyTorch, TensorFlow, Machine Learning, AI, AWS, Linux, Git required.'
            },
            {
                'title': 'Full Stack Python Developer',
                'description': 'Django, React, PostgreSQL, Docker, CI/CD, Agile, AWS or Azure experience needed.'
            }
        ]
        
        print("\n🔍 Processing sample job listings...\n")
        
        for job in demo_jobs:
            self.job_titles.append(job['title'])
            self.extract_skills(job['description'])
            print(f"   ✓ Processed: {job['title']}")
    
    def extract_skills(self, text):
        """
        Text se skills extract karta hai
        
        Parameters:
        - text: Job description ya koi bhi text
        """
        # Text ko lowercase mein convert karo for case-insensitive matching
        text_lower = text.lower()
        
        # Har skill check karo
        for skill in SKILLS_TO_TRACK:
            # Regex use karke skill dhundo (word boundary ke saath)
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                self.all_skills_found.append(skill)
    
    def analyze_skills(self):
        """
        Skills ki frequency count karta hai aur top skills return karta hai
        """
        if not self.all_skills_found:
            return []
        
        # Counter use karke frequency count karo
        skill_counts = Counter(self.all_skills_found)
        
        # Top 5 skills nikalo
        top_skills = skill_counts.most_common(5)
        
        return top_skills
    
    def generate_report(self):
        """
        Beautiful report generate karta hai
        """
        print("\n" + "="*60)
        print("📊 TECH SKILLS DEMAND REPORT")
        print("="*60)
        
        print(f"\n📈 Total Jobs Analyzed: {len(self.job_titles)}")
        print(f"🔍 Total Skills Mentions: {len(self.all_skills_found)}")
        print(f"🎯 Unique Skills Tracked: {len(SKILLS_TO_TRACK)}")
        
        # Top skills nikalo
        top_skills = self.analyze_skills()
        
        if top_skills:
            print("\n" + "-"*60)
            print("🏆 TOP 5 SKILLS IN DEMAND")
            print("-"*60)
            
            for rank, (skill, count) in enumerate(top_skills, 1):
                # Progress bar banaenge
                bar_length = int((count / top_skills[0][1]) * 30)
                bar = "█" * bar_length + "░" * (30 - bar_length)
                
                print(f"\n{rank}. {skill}")
                print(f"   {bar} {count} mentions")
                print(f"   Demand Score: {count}")
        else:
            print("\n⚠ No skills found in the analyzed jobs.")
        
        # Additional insights
        if self.job_titles:
            print("\n" + "-"*60)
            print("💼 SAMPLE JOB TITLES FOUND")
            print("-"*60)
            for i, title in enumerate(self.job_titles[:5], 1):
                print(f"{i}. {title}")
        
        # All skills frequency
        if self.all_skills_found:
            skill_counts = Counter(self.all_skills_found)
            print("\n" + "-"*60)
            print("📋 ALL SKILLS FREQUENCY")
            print("-"*60)
            for skill, count in skill_counts.most_common(10):
                print(f"   • {skill}: {count}")
        
        print("\n" + "="*60)
        print("✅ Analysis Complete!")
        print("="*60 + "\n")
    
    def save_report(self, filename="skills_report.txt"):
        """
        Report ko file mein save karta hai
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("TECH SKILLS DEMAND REPORT\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"Total Jobs Analyzed: {len(self.job_titles)}\n")
            f.write(f"Total Skills Mentions: {len(self.all_skills_found)}\n\n")
            
            top_skills = self.analyze_skills()
            
            if top_skills:
                f.write("-"*60 + "\n")
                f.write("TOP 5 SKILLS IN DEMAND\n")
                f.write("-"*60 + "\n\n")
                
                for rank, (skill, count) in enumerate(top_skills, 1):
                    f.write(f"{rank}. {skill}: {count} mentions\n")
            
            # All skills
            if self.all_skills_found:
                skill_counts = Counter(self.all_skills_found)
                f.write("\n" + "-"*60 + "\n")
                f.write("ALL SKILLS FREQUENCY\n")
                f.write("-"*60 + "\n\n")
                for skill, count in skill_counts.most_common():
                    f.write(f"{skill}: {count}\n")
        
        print(f"💾 Report saved to {filename}")


# ====================
# MAIN FUNCTION
# ====================
def main():
    """
    Main function - yahan se program start hota hai
    """
    print("\n" + "="*60)
    print("🚀 TECH SKILLS DEMAND CHECKER")
    print("="*60)
    
    # Scraper object banao
    scraper = TechSkillsScraper()
    
    # User ko options do
    print("\nSelect data source:")
    print("1. Scrape Indeed.com (Real-time data)")
    print("2. Use Sample Data (Faster, for testing)")
    
    try:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        
        if choice == "1":
            # Indeed scraping
            search = input("Enter job title to search (default: Python Developer): ").strip()
            if not search:
                search = "Python Developer"
            
            location = input("Enter location (default: India): ").strip()
            if not location:
                location = "India"
            
            pages = input("How many pages to scrape? (default: 3): ").strip()
            try:
                pages = int(pages) if pages else 3
            except:
                pages = 3
            
            scraper.scrape_indeed_jobs(search, location, pages)
        
        else:
            # Sample data use karo
            scraper.scrape_github_jobs()
        
        # Report generate karo
        scraper.generate_report()
        
        # Report save karo
        save = input("\n💾 Save report to file? (y/n): ").strip().lower()
        if save == 'y':
            scraper.save_report()
        
        print("\n✨ Thank you for using Tech Skills Demand Checker! ✨\n")
    
    except KeyboardInterrupt:
        print("\n\n❌ Program interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


# ====================
# RUN THE PROGRAM
# ====================
if __name__ == "__main__":
    main()
