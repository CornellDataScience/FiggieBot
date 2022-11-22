import './Searchbar.css'
import { useNavigate } from 'react-router-dom'
import React, { useState } from 'react'

export default function Searchbar({ client }) {
  const [username, setUsername] = useState('')
  const navigate = useNavigate()

  const handleSubmit = (e) => {
    e.preventDefault()
    navigate('/game')
    client.send(JSON.stringify({
      type: "add_player",
      data: {
        player_id: username
      }
    }))
  }

  return (
    <div className="searchbar">
      <form>
        <input
          class="username-input"
          type="text"
          placeholder="Enter a custom name"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <button
          class="play-button"
          onClick={(e) => handleSubmit(e)}
          placeholder="Play anonymously">
          {`Play as ${username}`}
        </button>
      </form>
    </div>
  )
}