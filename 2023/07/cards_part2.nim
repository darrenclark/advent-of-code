import std/os
import std/algorithm
import std/strutils
import std/parseutils
import std/strformat
import std/sequtils
import std/tables

# low to high value
type Card = enum c2, c3, c4, c5, c6, c7, c8, c9, cT, cJ, cQ, cK, cA

# low to high value
type
  HandType = enum
    htHighCard,
    htOnePair,
    htTwoPair,
    htThreeOfAKind,
    htFullHouse,
    htFourOfAKind,
    htFiveOfAKind

type
  Hand = object
    cards: seq[Card]
    bid: int
    handType: HandType

proc `<`(x, y: Hand): bool =
  if x.handType < y.handType:
    return true
  elif x.handType == y.handType:
    for i, xc in x.cards:
      if xc < y.cards[i]:
        return true
      elif xc > y.cards[i]:
        return false

  return false

proc parseCard(c: char): Card =
  case c
  of '2': return c2
  of '3': return c3
  of '4': return c4
  of '5': return c5
  of '6': return c6
  of '7': return c7
  of '8': return c8
  of '9': return c9
  of 'T': return cT
  of 'J': return cJ
  of 'Q': return cQ
  of 'K': return cK
  of 'A': return cA
  else: quit(fmt"unexpected card char: {c}", 1)

proc determineType(cards: seq[Card]): HandType =
  var counts = initCountTable[Card]()
  for card in cards:
    counts.inc(card)

  if counts.len() == 1:
    return htFiveOfAKind
  elif counts.len() == 2:
    let (_, c) = counts.largest()
    if c == 4:
      return htFourOfAKind
    else:
      return htFullHouse
  else:
    let (_, c) = counts.largest()

    if c == 3:
      return htThreeOfAKind
    elif c == 2:
      var numPairs = 0
      for c in counts.values:
        if c == 2: numPairs += 1

      return if numPairs >= 2: htTwoPair else: htOnePair
    else:
      return htHighCard

proc parseInput(inputPath: string): seq[Hand] =
  for line in lines(inputPath):
    let parts = split(line, " ")
    let handStr = parts[0]
    var bid = 0
    doAssert parseInt(parts[1], bid) != 0

    let cards = map(handStr, parseCard)
    result.add(Hand(cards: cards, bid: bid, handType: determineType(cards)))

proc main() =
  let params = commandLineParams()
  if params.len() != 1:
    quit("expected args: path/to/input.txt", 1)

  var hands = parseInput(params[0])
  hands.sort()

  var winnings = 0
  for i, h in hands:
    winnings += h.bid * (i+1)

  echo "Winnings: ", winnings

main()
