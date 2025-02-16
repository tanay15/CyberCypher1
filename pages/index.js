import { useState } from 'react'
import { useRouter } from 'next/router'

export default function Home() {
  const [industry, setIndustry] = useState('')
  const router = useRouter()

  const handleSubmit = (e) => {
    e.preventDefault()
    if (industry) {
      // Save the industry in local storage for later use
      localStorage.setItem('industry', industry)
      router.push('/chat')
    }
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Welcome to Founder Chatbot</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="industry">Enter your startup industry:</label>
        <br />
        <input
          id="industry"
          type="text"
          value={industry}
          onChange={(e) => setIndustry(e.target.value)}
          required
          style={{ margin: '1rem 0', padding: '0.5rem' }}
        />
        <br />
        <button type="submit" style={{ padding: '0.5rem 1rem' }}>
          Start Chat
        </button>
      </form>
    </div>
  )
}
