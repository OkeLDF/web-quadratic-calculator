const btnCalc = document.getElementById('btnCalc')

const aInput = document.getElementById('a')
const bInput = document.getElementById('b')
const cInput = document.getElementById('c')

const delta = document.getElementById('delta')
const n_results = document.getElementById('n_results')
const x1 = document.getElementById('x1')
const x2 = document.getElementById('x2')

btnCalc.addEventListener('click', () => {
    fetch('https://okeldf.pythonanywhere.com/', {
        method: 'POST',
        body: JSON.stringify({
            a: aInput.value,
            b: bInput.value,
            c: cInput.value,
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
        .then((response) => response.json())
        .then((json) => {
            delta.innerHTML = `delta = ${json.delta}`
            n_results.innerHTML = `n results = ${json.n_results}`

            if(json.complex){
                const real = json.real
                const im = json.imaginary

                x1.innerHTML = `x1 = ${real} + ${im} * i`
                x2.innerHTML = `x2 = ${real} - ${im} * i`
            }
            else {
                x1.innerHTML = `x1 = ${json.x1}`
                
                if(json.n_results == 2){
                    x2.innerHTML = `x2 = ${json.x2}`
                }
            }
        })
})
