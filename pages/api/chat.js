export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { message } = req.body

    // Call OpenRouter API for advisor response.
    // In production, store your API key in the environment variable.
    const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY
    const url = 'https://openrouter.ai/api/v1/chat/completions'

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
            {
              role: 'system',
              content: 'You are a startup advisor focusing on practical, actionable advice.'
            },
            { role: 'user', content: message }
          ],
          temperature: 0.7
        })
      })

      const data = await apiRes.json()
      const advisorReply = data.choices[0]?.message?.content?.trim() || 'No response.'
      res.status(200).json({ response: advisorReply })
    } catch (error) {
      console.error('Error in chat API:', error)
      res.status(500).json({ response: 'I encountered an error. Please try again.' })
    }
  } else {
    res.status(405).json({ message: 'Method not allowed' })
  }
}
