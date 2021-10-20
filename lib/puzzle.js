// select all the tiles
const tiles = document.querySelectorAll('td');

// check if a tile have an empty neighbour
const canMove = (tile) => {
  const tileColumn = tile.cellIndex;
  const tileRow = tile.parentElement.rowIndex;
  const emptyTile = document.querySelector('.empty');
  const emptyTileColumn = emptyTile.cellIndex;
  const emptyTileRow = emptyTile.parentElement.rowIndex;

  return (tileColumn === emptyTileColumn && tileRow === emptyTileRow + 1) ||
         (tileColumn === emptyTileColumn && tileRow === emptyTileRow - 1) ||
         (tileRow === emptyTileRow && tileColumn === emptyTileColumn + 1) ||
         (tileRow === emptyTileRow && tileColumn === emptyTileColumn - 1);
};

// Move the tile
const moveTile = (element) => {
  // select the empty place
  const emptyTile = document.querySelector('.empty');
  emptyTile.innerHTML = element.innerHTML;
  emptyTile.classList.remove('empty');
  element.innerHTML = '0';
  element.classList.add('empty');
};

const checkIfPlayerWins = () => {
  const tilesOrder = Array.from(document.querySelectorAll('td')).map(e => Number.parseInt(e.innerHTML, 10));
  if (tilesOrder.join() === "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,NaN") {
    alert("You win!");
  }
};

const resetListeners = () => {
  // add event listener on each tiles
  const tiles = document.querySelectorAll('td');
  tiles.forEach((tile) => {
    tile.addEventListener('click', () => {
      console.log('clicked')
      if (canMove(tile)) {
        moveTile(tile);
        checkIfPlayerWins();
      }
    });
  });
}
resetListeners()

/// Python 8puzzle api

document.querySelector('#callgreedy').addEventListener('click', () => {
  const rows = document.querySelectorAll('tr');
  let tiles = []
  rows.forEach(row => {
    tiles.push(row.innerText.split('\n'))
  })

  fetch('http://localhost:8800/start', {
    'method': 'POST',
    'body': JSON.stringify({ 'tiles': tiles, 'algo': 'greedy' })
  })
  .then(res => res.json())
  .then(data => {
    const states = data.states
    // console.log(states.length)
    states.forEach((state, i) => {
      setTimeout(function() {
        displayBoard(state);
        resetListeners()
      }, i * 300)
    })
  })
})

document.querySelector('#callbfs').addEventListener('click', () => {
  const rows = document.querySelectorAll('tr');
  let tiles = []
  rows.forEach(row => {
    tiles.push(row.innerText.split('\n'))
  })

  fetch('http://localhost:8800/start', {
    'method': 'POST',
    'body': JSON.stringify({ 'tiles': tiles, 'algo': 'bfs' })
  })
  .then(res => res.json())
  .then(data => {
    const states = data.states
    // console.log(states.length)
    states.forEach((state, i) => {
      setTimeout(function() {
        displayBoard(state);
        resetListeners()
      }, i * 300)
    })
  })
})

const displayBoard = (board) => {
  table = document.querySelector('table')
  table.innerHTML = ""
  console.log(board.length)
  board.forEach(row => {
    let rowHTML = row.map(cell => {
      if (cell == 0) {
        return `<td class='empty'>${cell}</td>`
      }
      return `<td>${cell}</td>`
    })
    table.insertAdjacentHTML('beforeend', rowHTML)
  })
}

// document.querySelector('#play').addEventListener('click', () => {
//   fetch('http://localhost:8800/')
//   .then(res => res.json())
//   .then(data => {
//     const states = data.states
//     // console.log(states.length)
//     states.forEach((state, i) => {
//       setTimeout(function() {
//         displayBoard(state);
//       }, i * 300)
//     })
//   })
// })
