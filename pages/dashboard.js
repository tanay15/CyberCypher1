import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'

export default function Dashboard() {
  const router = useRouter()
  const [dashboard, setDashboard] = useState('')

  useEffect(() => {
    const savedConversation = localStorage.getItem('conversation')
    const savedIndustry = localStorage.getItem('industry')
    if (!savedConversation || !savedIndustry) {
      router.push('/')
      return
    }

    const conversation = JSON.parse(savedConversation)
    // Call our API route to generate the dashboard
    fetch('/api/dashboard', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ conversation, industry: savedIndustry })
    })
      .then((res) => res.json())
      .then((data) => setDashboard(data.dashboard))
      .catch((err) => {
        console.error('Error generating dashboard:', err)
        setDashboard('Error generating dashboard.')
      })
  }, [router])

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Startup Dashboard</h1>
      <pre style={{ background: '#f4f4f4', padding: '1rem' }}>{dashboard}</pre>
      <button onClick={() => router.push('/')} style={{ padding: '0.5rem 1rem' }}>
        Start Over
      </button>
    </div>
  )
}
