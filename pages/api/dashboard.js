export default async function handler(req, res) {
    if (req.method === 'POST') {
      const { conversation, industry } = req.body
  
      // For dashboard generation, we create a prompt that asks the analysis engine
      // to analyze the conversation and produce a dashboard.
      const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY
      const url = 'https://openrouter.ai/api/v1/chat/completions'
      const prompt = `
  Analyze the following startup conversation:
  ${JSON.stringify(conversation, null, 2)}
  
  Identify:
  1. Core problem statement
  2. Target market
  3. Technical stack components
  4. Revenue model
  5. Competitive advantages
  
  Now, generate a startup dashboard that includes:
  - Market Analysis
  - Legal Requirements
  - Growth Strategy
  
  Industry: ${industry}
      `.trim()
  
      try {
        const apiRes = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${OPENROUTER_API_KEY}`
          },
          body: JSON.stringify({
            model: 'gpt-3.5-turbo',
            messages: [
              { role: 'system', content: 'You are a startup analysis engine.' },
              { role: 'user', content: prompt }
            ],
            temperature: 0.5
          })
        })
  
        const data = await apiRes.json()
        const dashboardText = data.choices[0]?.message?.content?.trim() || 'Dashboard generation failed.'
        res.status(200).json({ dashboard: dashboardText })
      } catch (error) {
        console.error('Error in dashboard API:', error)
        res.status(500).json({ dashboard: 'Error generating dashboard.' })
      }
    } else {
      res.status(405).json({ message: 'Method not allowed' })
    }
  }
  