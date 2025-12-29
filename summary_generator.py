"""
Summary Generator Module
Generates summaries in Chinese using OpenAI API
"""
import openai
import os


class SummaryGenerator:
    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
        self.model = model
        
    def generate_summary(self, text, language="Chinese"):
        """Generate summary from text"""
        if not text or not text.strip():
            return ""
            
        if not self.api_key:
            return "请配置 OpenAI API 密钥以生成摘要 / Please configure OpenAI API key to generate summary"
            
        try:
            prompt = f"""Please summarize the following meeting transcript in {language}. 
Focus on key points, decisions, and action items.

Transcript:
{text}

Summary in {language}:"""

            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a professional meeting summarizer. Generate concise summaries in {language}."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
            
        except Exception as e:
            print(f"Summary generation error: {e}")
            return f"摘要生成错误: {str(e)} / Summary generation error: {str(e)}"
            
    def generate_summary_from_segments(self, segments, language="Chinese"):
        """Generate summary from multiple text segments"""
        combined_text = "\n".join([seg["text"] for seg in segments if seg.get("text")])
        return self.generate_summary(combined_text, language)
