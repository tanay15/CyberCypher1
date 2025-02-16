import os
import json
import requests
from textwrap import dedent
from openai import OpenAI

# --- Configuration ---
OPENROUTER_API_KEY = "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"
SERPER_API_KEY = "e37a638aabb0308a6604184041e58fab186edff3"
FINNHUB_API_KEY = "cuomlnhr01qve8pu8fd0cuomlnhr01qve8pu8fdg"

# Initialize OpenRouter client
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    default_headers={"HTTP-Referer": "http://localhost:8000"}
)

def perform_web_search(query):
    """Perform real-time web search using Serper API"""
    try:
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Search API error: {str(e)}")
        return {"organic": [], "news": []}

def get_market_size_estimate(industry):
    """Get market size estimate using web search"""
    try:
        search_query = f"{industry} market size 2024 billion revenue"
        results = perform_web_search(search_query)
        
        for result in results.get('organic', []):
            description = result.get('snippet', '').lower()
            if 'market size' in description or 'billion' in description or 'million' in description:
                return result.get('snippet', 'Market size information not available')
        
        return "Market size information not available"
    except Exception as e:
        print(f"Market size estimation error: {str(e)}")
        return "Market size information not available"

def analyze_market_landscape(industry):
    """Enhanced market analysis using web data"""
    try:
        competitors_search = perform_web_search(f"top companies startups {industry} 2024")
        trends_search = perform_web_search(f"latest trends innovations {industry} 2024")
        market_size = get_market_size_estimate(industry)
        
        competitors = []
        for result in competitors_search.get('organic', [])[:5]:
            if 'title' in result:
                name = result['title'].split('-')[0].strip()
                if len(name) > 5:
                    competitors.append(name)
        
        trends = []
        for result in trends_search.get('organic', [])[:3]:
            if 'title' in result:
                trends.append(result['title'])
        
        return {
            'competitors': competitors if competitors else ["No competitor data available"],
            'market_size': market_size,
            'trends': trends if trends else ["No trend data available"]
        }
    except Exception as e:
        print(f"Market analysis error: {str(e)}")
        return {
            'competitors': ["Unable to fetch competitor data"],
            'market_size': "Market size information not available",
            'trends': ["Unable to fetch trend data"]
        }

def generate_legal_requirements(industry, country="US"):
    """Enhanced legal requirements generation"""
    try:
        regulatory_search = perform_web_search(f"{industry} regulations compliance requirements {country}")
        license_search = perform_web_search(f"{industry} business licenses permits {country}")
        
        requirements = []
        
        for result in regulatory_search.get('organic', [])[:3]:
            if 'title' in result:
                requirements.append(f"Regulatory: {result['title']}")
        
        for result in license_search.get('organic', [])[:2]:
            if 'title' in result:
                requirements.append(f"Licensing: {result['title']}")
        
        return requirements if requirements else ["Please consult with a legal professional for specific requirements"]
    except Exception as e:
        print(f"Legal requirements error: {str(e)}")
        return ["Unable to fetch legal requirements"]

# --- Startup Advisor Class ---
class StartupAdvisor:
    """Main class for handling startup analysis and conversation"""
    def __init__(self):
        self.conversation_history = []
        self.idea_details = {}
    
    def analyze_conversation(self):
        """Analyze conversation history using GPT-3.5"""
        try:
            analysis_prompt = f"""
            Analyze this startup idea conversation and extract key components:
            {self.conversation_history}
            
            Identify:
            1. Core problem statement
            2. Target market
            3. Technical stack components
            4. Revenue model
            5. Competitive advantages
            """
            
            response = openrouter_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a startup analysis engine"},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Conversation analysis error: {str(e)}")
            return "Unable to analyze conversation"
    
    def generate_growth_strategy(self):
        """Generate AI-powered growth recommendations"""
        try:
            market_data = analyze_market_landscape(self.idea_details.get('industry', ''))
            
            strategy_prompt = f"""
            Generate growth strategy for startup with these details:
            {self.idea_details}
            
            Market analysis:
            {market_data}
            
            Provide specific, actionable recommendations for:
            1. Market entry strategy
            2. Customer acquisition
            3. Revenue growth
            4. Competitive positioning
            5. Scaling operations
            """
            
            response = openrouter_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a growth strategy expert"},
                    {"role": "user", "content": strategy_prompt}
                ],
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Growth strategy error: {str(e)}")
            return "Unable to generate growth strategy"

# --- Dashboard Class ---
class FounderDashboard:
    """Class for generating the final startup dashboard"""
    def __init__(self, advisor):
        self.advisor = advisor
        self.market_data = None
        self.legal_requirements = None
    
    def generate_dashboard(self):
        """Generate comprehensive dashboard with all analyses"""
        try:
            self.market_data = analyze_market_landscape(
                self.advisor.idea_details.get('industry', '')
            )
            
            self.legal_requirements = generate_legal_requirements(
                self.advisor.idea_details.get('industry', '')
            )
            
            analysis = self.advisor.analyze_conversation()
            growth_strategy = self.advisor.generate_growth_strategy()
            
            return {
                "market_analysis": self.market_data,
                "legal_requirements": self.legal_requirements,
                "financial_analysis": analysis,
                "growth_strategy": growth_strategy
            }
        except Exception as e:
            print(f"Dashboard generation error: {str(e)}")
            return {}

def format_dashboard_output(results):
    """Format dashboard output in a readable way"""
    market_analysis = results.get('market_analysis', {})
    legal_reqs = results.get('legal_requirements', [])
    
    return dedent(f"""
    === Market Analysis ===
    Industry Overview:
    {market_analysis.get('market_size', 'Market size information not available')}
    
    Top Competitors:
    {chr(10).join('- ' + comp for comp in market_analysis.get('competitors', []))}
    
    Key Industry Trends:
    {chr(10).join('- ' + trend for trend in market_analysis.get('trends', []))}
    
    === Legal Requirements ===
    {chr(10).join('- ' + req for req in legal_reqs)}
    
    === Growth Strategy ===
    {results.get('growth_strategy', 'Unable to generate growth strategy')}
    """)

def main():
    print("🚀 Welcome to Next-Gen Founder Arena")
    advisor = StartupAdvisor()
    
    try:
        print("\nWhat industry is your startup in? (Please be specific, e.g., 'Mobile Healthcare Apps' or 'Sustainable Fashion E-commerce')")
        industry = input("Industry: ")
        advisor.idea_details['industry'] = industry
        
        print("\nTell me about your startup idea (type 'exit' to finish):")
        while True:
            user_input = input("\nFounder: ")
            advisor.conversation_history.append(user_input)
            
            if "exit" in user_input.lower():
                break
            
            try:
                response = openrouter_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a startup advisor focusing on practical, actionable advice."},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7
                )
                print(f"\nAdvisor: {response.choices[0].message.content}")
            except Exception as e:
                print(f"\nAdvisor: I apologize, but I encountered an error. Please try again.")
        
        print("\nGenerating your startup dashboard...")
        dashboard = FounderDashboard(advisor)
        results = dashboard.generate_dashboard()
        
        print("\n📊 Final Startup Dashboard")
        print(format_dashboard_output(results))
        
        with open("startup_report.json", "w") as f:
            json.dump(results, f, indent=2)
        print("\nDetailed report saved to 'startup_report.json'")
            
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()