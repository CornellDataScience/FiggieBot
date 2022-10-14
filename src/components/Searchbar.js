import './Searchbar.css'

import React, { useState } from 'react'

export default function Searchbar() {
    const [username, setUsername] = useState('')

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
            placeholder="Play anonymously">
                {`Play as ${username}`}
            </button>
        </form>
    </div>
  )
}
