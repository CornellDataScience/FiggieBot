import React from 'react'
import './Game.css'
import { useState } from 'react'
// import Txtandbutton from '../../components/Txtandbutton'

function Game() {
    const [orderBook, setOrderBook] = useState({
        bids: { spades: 0, hearts: 0, diamonds: 0, clubs: 0 },
        offers: { spades: 0, hearts: 0, diamonds: 0, clubs: 0 }
    })

    const [spadeBid, setSpadeBid] = useState(0)
    const [spadeOffer, setSpadeOffer] = useState(0)
    const [heartBid, setHeartBid] = useState(0)
    const [heartOffer, setHeartOffer] = useState(0)
    const [diamondBid, setDiamondBid] = useState(0)
    const [diamondOffer, setDiamondOffer] = useState(0)
    const [clubBid, setClubBid] = useState(0)
    const [clubOffer, setClubOffer] = useState(0)

    const handleClickSB = (e) => {
        e.preventDefault()
        const copy = { ...orderBook }
        copy.bids.spades = spadeBid
        setOrderBook(copy)
    }

    const handleClickSO = (e) => {
        e.preventDefault()
        const copy = { ...orderBook }
        copy.offers.spades = spadeOffer
        setOrderBook(copy)
    }

    const handleClickHB = (e) => {
        e.preventDefault()
        const copy = { ...orderBook }
        copy.bids.hearts = heartBid
        setOrderBook(copy)
    }

    const handleClickHO = (e) => {
        e.preventDefault()
        const copy = { ...orderBook }
        copy.offers.hearts = heartOffer
        setOrderBook(copy)
    }

    const handleClickDB = (e) => {
        e.preventDefault()
        const copy = { ...orderBook }
        copy.bids.diamonds = diamondBid
        setOrderBook(copy)
    }

    const handleClickDO = (e) => {
        e.preventDefault()
        const copy = { ...orderBook }
        copy.offers.diamonds = diamondOffer
        setOrderBook(copy)
    }

    const handleClickCB = (e) => {
        e.preventDefault()
        const copy = { ...orderBook }
        copy.bids.clubs = clubBid
        setOrderBook(copy)
    }

    const handleClickCO = (e) => {
        e.preventDefault()
        const copy = { ...orderBook }
        copy.offers.clubs = clubOffer
        setOrderBook(copy)
    }

    return (
        <div className="game">
            {/* <Txtandbutton /> */}
            <h1>Spades</h1>
            <form>
                <p1>Current: {orderBook.bids.spades}</p1>
                <input value={spadeBid} onChange={(e) => setSpadeBid(e.target.value)} type="number" />
                <button onClick={handleClickSB} >Bid</button>
                <br />
                <p1>Current: {orderBook.offers.spades}</p1>
                <input value={spadeOffer} onChange={(e) => setSpadeOffer(e.target.value)} type="number" />
                <button onClick={handleClickSO} >Offer</button>
            </form>
            <h1>Clubs</h1>
            <form>
                <p1>Current: {orderBook.bids.clubs}</p1>
                <input value={clubBid} onChange={(e) => setClubBid(e.target.value)} type="number" />
                <button onClick={handleClickCB} >Bid</button>
                <br />
                <p1>Current: {orderBook.offers.clubs}</p1>
                <input value={clubOffer} onChange={(e) => setClubOffer(e.target.value)} type="number" />
                <button onClick={handleClickCO} >Offer</button>
            </form>
            <h1>Diamonds</h1>
            <form>
                <p1>Current: {orderBook.bids.diamonds}</p1>
                <input value={diamondBid} onChange={(e) => setDiamondBid(e.target.value)} type="number" />
                <button onClick={handleClickDB} >Bid</button>
                <br />
                <p1>Current: {orderBook.offers.diamonds}</p1>
                <input value={diamondOffer} onChange={(e) => setDiamondOffer(e.target.value)} type="number" />
                <button onClick={handleClickDO} >Offer</button>
            </form>
            <h1>Hearts</h1>
            <form>
                <p1>Current: {orderBook.bids.hearts}</p1>
                <input value={heartBid} onChange={(e) => setHeartBid(e.target.value)} type="number" />
                <button onClick={handleClickHB} >Bid</button>
                <br />
                <p1>Current: {orderBook.offers.hearts}</p1>
                <input value={heartOffer} onChange={(e) => setHeartOffer(e.target.value)} type="number" />
                <button onClick={handleClickHO} >Offer</button>
            </form>
        </div>
    )
}

export default Game