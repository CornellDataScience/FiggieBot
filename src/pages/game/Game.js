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
        const copy = orderBook
        copy.bids.spades = spadeBid
        setOrderBook(copy)
        console.log(copy)
    }

    const handleClick = (e) => {
        e.preventDefault()
        const copy = orderBook
        copy.bids.spades = spadeBid
        setOrderBook(copy)
    }


    // function handleClick(params) {
    //     preventDefault()
    //     if (params[0] == "s" && params[1] == "b") {
    //         const copy = orderBook
    //         copy.bids.spades = spadeBid
    //         setOrderBook(copy)
    //     }
    // }

    return (
        <div className="game">
            {/* <Txtandbutton /> */}
            <p1>Spades</p1>
            <form>
                <p1>Current: {orderBook.bids.spades}</p1>
                <input value={spadeBid} onChange={(e) => setSpadeBid(e.target.value)} />
                <button onClick={(e) => handleClickSB(e)} >Bid</button>
                <p1>Current: {orderBook.offers.spades}</p1>
                <input value={spadeOffer} onChange={(e) => setSpadeOffer(e.target.value)} />
                <button>Offer</button>
            </form>
            <p1>Clubs</p1>
            <form>
                <p1>Current: {orderBook.bids.clubs}</p1>
                <input value={clubBid} onChange={(e) => setClubBid(e.target.value)} />
                <button onClick={handleClick} >Bid</button>
                <p1>Current: {orderBook.offers.clubs}</p1>
                <input value={clubOffer} onChange={(e) => setClubOffer(e.target.value)} />
                <button>Offer</button>
            </form>
            <p1>Diamonds</p1>
            <form>
                <p1>Current: {orderBook.bids.diamonds}</p1>
                <input value={diamondBid} onChange={(e) => setDiamondBid(e.target.value)} />
                <button onClick={handleClick} >Bid</button>
                <p1>Current: {orderBook.offers.diamonds}</p1>
                <input value={diamondOffer} onChange={(e) => setDiamondOffer(e.target.value)} />
                <button>Offer</button>
            </form>
            <p1>Hearts</p1>
            <form>
                <p1>Current: {orderBook.bids.hearts}</p1>
                <input value={heartBid} onChange={(e) => setHeartBid(e.target.value)} />
                <button onClick={handleClick} >Bid</button>
                <p1>Current: {orderBook.offers.hearts}</p1>
                <input value={heartOffer} onChange={(e) => setHeartOffer(e.target.value)} />
                <button>Offer</button>
            </form>
        </div>
    )
}

export default Game