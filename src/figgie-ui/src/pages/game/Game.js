import React from 'react'
import './Game.css'
import { useState, useEffect } from 'react'

function Game({ client }) {
    useEffect(() => {
        client.onopen = () => {
            console.log('ws opened');
            client.send(JSON.stringify({ type: "request_state", data: {} }))
        }
        client.onclose = () => console.log('ws closed');

        client.onmessage = e => {
            const message = JSON.parse(e.data);
            if (message.type === "update_game") {
                setGameState(message.data);
                setNumPlayers(() => calcPlayers());
            }
            if (message.type === "add_player") {
                const copy = { ...gameState, player: { ...gameState.player, player_id: message.data.player_id } }
                setGameState(copy);
            }
        };
    }, [client]);

    const [gameState, setGameState] = useState({
        round_number: 0,
        time: 0,
        player: {
            player_id: "",
            balance: 0,
            hand: {
                hearts: 0,
                diamonds: 0,
                clubs: 0,
                spades: 0
            }
        },
        players: [
            { player_id: "", balance: 0 },
            { player_id: "", balance: 0 },
            { player_id: "", balance: 0 },
            { player_id: "", balance: 0 }
        ],
        order_book: {
            bids: {
                hearts: { order_id: -1, player_id: "", suit: "", price: 0 },
                diamonds: { order_id: -1, player_id: "", suit: "", price: 0 },
                clubs: { order_id: -1, player_id: "", suit: "", price: 0 },
                spades: { order_id: -1, player_id: "", suit: "", price: 0 }
            },
            offers: {
                hearts: { order_id: -1, player_id: "", suit: "", price: 0 },
                diamonds: { order_id: -1, player_id: "", suit: "", price: 0 },
                clubs: { order_id: -1, player_id: "", suit: "", price: 0 },
                spades: { order_id: -1, player_id: "", suit: "", price: 0 }
            }
        }
    })

    const [spadeBid, setSpadeBid] = useState(0)
    const [spadeOffer, setSpadeOffer] = useState(0)
    const [heartBid, setHeartBid] = useState(0)
    const [heartOffer, setHeartOffer] = useState(0)
    const [diamondBid, setDiamondBid] = useState(0)
    const [diamondOffer, setDiamondOffer] = useState(0)
    const [clubBid, setClubBid] = useState(0)
    const [clubOffer, setClubOffer] = useState(0)


    const calcPlayers = () => {
        let count = 0;
        let players = gameState.players
        for (let i = 0; i < players.length; i++) {
            if (players[i].player_id !== "") {
                count += 1
            }
        }
        return count
    }

    const startGame = () => {
        client.send(JSON.stringify({
            type: "start_game",
            data: { "player_id": gameState.player.player_id }
        }))
    }

    const [numPlayers, setNumPlayers] = useState(calcPlayers)

    const handleClickSB = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "place_order", data: { player_id: gameState.player.player_id, is_bid: true, suit: "spades", price: Number(spadeBid) } }))
    }

    const handleClickSO = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "place_order", data: { player_id: gameState.player.player_id, is_bid: false, suit: "spades", price: Number(spadeOffer) } }))
    }

    const handleClickHB = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "place_order", data: { player_id: gameState.player.player_id, is_bid: true, suit: "hearts", price: Number(heartBid) } }))
    }

    const handleClickHO = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "place_order", data: { player_id: gameState.player.player_id, is_bid: false, suit: "hearts", price: Number(heartOffer) } }))
    }

    const handleClickDB = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "place_order", data: { player_id: gameState.player.player_id, is_bid: true, suit: "diamonds", price: Number(diamondBid) } }))
    }

    const handleClickDO = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "place_order", data: { player_id: gameState.player.player_id, is_bid: false, suit: "diamonds", price: Number(diamondOffer) } }))
    }

    const handleClickCB = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "place_order", data: { player_id: gameState.player.player_id, is_bid: true, suit: "clubs", price: Number(clubBid) } }))
    }

    const handleClickCO = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "place_order", data: { player_id: gameState.player.player_id, is_bid: false, suit: "clubs", price: Number(clubOffer) } }))
    }

    const acceptSB = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "accept_order", data: { "accepter_id": gameState.player.player_id, is_bid: true, suit: "spades" } }))
    }

    const acceptSO = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "accept_order", data: { "accepter_id": gameState.player.player_id, is_bid: false, suit: "spades" } }))
    }

    const acceptHB = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "accept_order", data: { "accepter_id": gameState.player.player_id, is_bid: true, suit: "hearts" } }))
    }

    const acceptHO = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "accept_order", data: { "accepter_id": gameState.player.player_id, is_bid: false, suit: "hearts" } }))
    }

    const acceptDB = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "accept_order", data: { "accepter_id": gameState.player.player_id, is_bid: true, suit: "diamonds" } }))
    }

    const acceptDO = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "accept_order", data: { "accepter_id": gameState.player.player_id, is_bid: false, suit: "diamonds" } }))
    }

    const acceptCB = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "accept_order", data: { "accepter_id": gameState.player.player_id, is_bid: true, suit: "clubs" } }))
    }

    const acceptCO = (e) => {
        e.preventDefault()
        client.send(JSON.stringify({ type: "accept_order", data: { "accepter_id": gameState.player.player_id, is_bid: false, suit: "clubs" } }))
    }

    return (
        <div className="game">
            <p1>Players Connected: {numPlayers}</p1>
            <div>
                <button onClick={startGame}>Start Game</button>
            </div>
            <div>
                <p1>Timer: {gameState.time}</p1>
            </div>
            <div>
                <p1>Hearts: {gameState.player.hand.hearts} | </p1>
                <p1>Diamonds: {gameState.player.hand.diamonds} | </p1>
                <p1>Clubs: {gameState.player.hand.clubs} | </p1>
                <p1>Spades: {gameState.player.hand.spades} | </p1>
                <p1>Balance: {gameState.player.balance}</p1>
            </div>
            <h1>Spades</h1>
            <form>
                <p1>Current: {gameState.order_book.bids.spades.price}</p1>
                <input value={spadeBid} onChange={(e) => setSpadeBid(e.target.value)} type="number" />
                <div>
                    <button onClick={handleClickSB} >Bid</button>
                    <button onClick={acceptSB}>Accept Order</button>
                </div>
                <br />
                <p1>Current: {gameState.order_book.offers.spades.price}</p1>
                <input value={spadeOffer} onChange={(e) => setSpadeOffer(e.target.value)} type="number" />
                <div>
                    <button onClick={handleClickSO} >Offer</button>
                    <button onClick={acceptSO}>Accept Order</button>
                </div>
            </form>
            <h1>Clubs</h1>
            <form>
                <p1>Current: {gameState.order_book.bids.clubs.price}</p1>
                <input value={clubBid} onChange={(e) => setClubBid(e.target.value)} type="number" />
                <div>
                    <button onClick={handleClickCB} >Bid</button>
                    <button onClick={acceptCB}>Accept Order</button>
                </div>
                <br />
                <p1>Current: {gameState.order_book.offers.clubs.price}</p1>
                <input value={clubOffer} onChange={(e) => setClubOffer(e.target.value)} type="number" />
                <div>
                    <button onClick={handleClickCO} >Offer</button>
                    <button onClick={acceptCO}>Accept Order</button>
                </div>
            </form>
            <h1>Diamonds</h1>
            <form>
                <p1>Current: {gameState.order_book.bids.diamonds.price}</p1>
                <input value={diamondBid} onChange={(e) => setDiamondBid(e.target.value)} type="number" />
                <div>
                    <button onClick={handleClickDB} >Bid</button>
                    <button onClick={acceptDB}>Accept Order</button>
                </div>
                <br />
                <p1>Current: {gameState.order_book.offers.diamonds.price}</p1>
                <input value={diamondOffer} onChange={(e) => setDiamondOffer(e.target.value)} type="number" />
                <div>
                    <button onClick={handleClickDO} >Offer</button>
                    <button onClick={acceptDO}>Accept Order</button>
                </div>
            </form>
            <h1>Hearts</h1>
            <form>
                <p1>Current: {gameState.order_book.bids.hearts.price}</p1>
                <input value={heartBid} onChange={(e) => setHeartBid(e.target.value)} type="number" />
                <div>
                    <button onClick={handleClickHB} >Bid</button>
                    <button onClick={acceptHB}>Accept Order</button>
                </div>
                <br />
                <p1>Current: {gameState.order_book.offers.hearts.price}</p1>
                <input value={heartOffer} onChange={(e) => setHeartOffer(e.target.value)} type="number" />
                <div>
                    <button onClick={handleClickHO} >Offer</button>
                    <button onClick={acceptHO}>Accept Order</button>
                </div>
            </form>
        </div>
    )
}

export default Game