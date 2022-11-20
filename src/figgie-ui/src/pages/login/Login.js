import React from 'react'
import './Login.css'
import Searchbar from '../../components/Searchbar'

export default function Login({ client }) {
  return (
    <div className="login">
      <img src="https://americas.figgie.com/landing-graphic-static-3d-logo.96941b71.png" />
      {<Searchbar client={client} />}
    </div>
  )
}
