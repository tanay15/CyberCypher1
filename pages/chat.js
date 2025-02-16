import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'

export default function Chat() {
  const router = useRouter()
  const [conversation, setConversation] = useState([])
  const [message, setMessage] = useState('')
  const [industry, setIndustry] = useState('')

  // On mount, check if industry is set; if not, redirect to index
  useEffect(() => {
    const savedIndustry = localStorage.getItem('industry')
    if (!savedIndustry) {
      router.push('/')
    } else {
      setIndustry(savedIndustry)
    }
  }, [router])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!message.trim()) return

    // Add the founder's message to the conversation
    const updatedConversation = [...conversation, { role: 'Founder', text: message }]
    setConversation(updatedConversation)

    // If founder types "exit", finish chat and go to dashboard
    if (message.trim().toLowerCase() === 'exit') {
      localStorage.setItem('conversation', JSON.stringify(updatedConversation))
      router.push('/dashboard')
      return
    }

    // Call our API route to get advisor response
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, industry })
      })
      const data = await res.json()
      const advisorReply = data.response || 'Sorry, something went wrong.'

      // Add the advisor's response to the conversation
      setConversation([...updatedConversation, { role: 'Advisor', text: advisorReply }])
      setMessage('')
    } catch (error) {
      console.error('Error fetching advisor response:', error)
      setConversation([
        ...updatedConversation,
        { role: 'Advisor', text: 'Error: Unable to get a response. Please try again.' }
      ])
      setMessage('')
    }
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Founder Chatbot</h1>
      <div
        style={{
          border: '1px solid #ccc',
          padding: '1rem',
          marginBottom: '1rem',
          maxHeight: '300px',
          overflowY: 'auto'
        }}
      >
        {conversation.map((msg, idx) => (
          <p key={idx}>
            <strong>{msg.role}:</strong> {msg.text}
          </p>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Type your message here..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          style={{ width: '80%', padding: '0.5rem' }}
          autoFocus
          required
        />
        <button type="submit" style={{ padding: '0.5rem 1rem', marginLeft: '0.5rem' }}>
          Send
        </button>
      </form>
      <br />
      <button
        onClick={() => {
          // Simulate finishing the chat by sending "exit"
          setMessage('exit')
          // Trigger form submission
          const fakeEvent = { preventDefault: () => {} }
          handleSubmit(fakeEvent)
        }}
        style={{ padding: '0.5rem 1rem', marginTop: '1rem' }}
      >
        Finish Chat and Generate Dashboard
      </button>
    </div>
  )
}
