
let cTotal = Snap.select('#pie-total')
let cServed = Snap.select('#pie-served')
let cTarget = Snap.select('#pie-target')
let fpc = Snap.select('#potential-customer')
let checkLeft = Snap.select('#check-left')
let checkRight = Snap.select('#check-right')

let flowchart = Snap.select('#flowchart-viewbox')
let isExpended: boolean = false
let viewboxPos: array = [
  "0 -100 600 1100",
  "0 55 600 1100",
  "0 200 600 1100",
  "0 230 600 1100",
  "0 540 600 1100",
  "0 800 600 1100"
]
class Agent {
  public stage: int
  public progress: int
  public max: int
  constructor(maxStage: int, initStage: int) {
    this.stage = initStage || 0
    this.progress = this.stage
    this.max = maxStage - 1
  }
  public nextStage(): void {
    (this.stage < this.max)? this.stage++ : console.log('at the maximun')
    this.progress = this.stage
    console.log('current Stage is : ' + this.stage)
    this._updateCircles()
  }
  public prevStage(): void {
    (this.stage > 0)? this.stage-- : console.log('at the minimun')
    console.log('current Stage is : ' + this.stage)
    this.progress = this.stage
    this._updateCircles()
  }
  public fullStage() {
    this.stage = this.max
    this._updateCircles()
  }
  public returnStage() {
    this.stage = this.progress
    this._updateCircles()
  }
  private _graphics(served: int, target: int, check: int): void {
    cServed.animate({opacity: served}, 400, mina.easeinout)
    cTarget.animate({opacity: target}, 400, mina.easeinout)
    checkLeft.animate({opacity: check}, 400, mina.easeinout)
    checkRight.animate({opacity: check}, 400, mina.easeinout)
  }
  private _updateCircles() {
    if(viewboxPos[this.stage]){
      flowchart.animate({viewBox: viewboxPos[this.stage]}, 500, mina.easeinout)
    }
    switch (this.stage) {
      case 0:
        this._graphics(0, 0, 0)
        break
      case 1:
        this._graphics(1, 0, 0)
        break
      case 2: 
        this._graphics(1, 0, 0)
        break
      case 3: 
        this._graphics(1, 0, 1)
        break
      case 4:
        this._graphics(1, 0, 1)
        break
      case 5:
        this._graphics(1, 1, 1)
        break
    }   
  }
  
  
}

let kentAgent = new Agent(viewboxPos.length);

// INITIALIZE graphic, hide/show/position needed graphic
function initSVG(): void {
  // top circles
  cTotal.animate({opacity: 1}, 500, mina.easein)
  // flowchart
  flowchart.attr({viewBox: viewboxPos[kentAgent.stage]})
  checkLeft.attr({opacity: 0})
  checkRight.attr({opacity: 0})
}

// EXPEND the whole graphic
function expendSVG(): void {
  kentAgent.fullStage()
  flowchart.animate({viewBox: "0 0 600 1100"}, 800, mina.easeinout)
}
function collapseSVG(): void {
  kentAgent.returnStage()
  flowchart.animate({viewBox: viewboxPos[kentAgent.stage]}, 400, mina.easeinout)
}
function disableBtn(p: boolean) {
  if(p) {
    $('#btn-prev').show('slow')
    $('#btn-next').show('slow')
  }else{
    $('#btn-prev').hide('slow')
    $('#btn-next').hide('slow')
  }
}

window.onload = function(){
  initSVG()
}

$('#btn-prev').on('click', ()=>{ 
  if(!isExpended) {
    kentAgent.prevStage()
    if (kentAgent.stage <= 0) {
      $('#btn-prev').addClass('disabled')
    }else{
      $('#btn-next').removeClass('disabled')
    }
  }
})
$('#btn-next').on('click', ()=>{ 
  if(!isExpended) kentAgent.nextStage()
  if (kentAgent.stage >= kentAgent.max) {
      $('#btn-next').addClass('disabled')
    }else{
      $('#btn-prev').removeClass('disabled')
    }
})
$('#svg-expand').on('click', ()=>{ 
  if (isExpended) {
    isExpended = false
    $('#svg-expand').removeClass('expanded')
    $('#svg-flowchart').removeClass('size')
    collapseSVG();
    disableBtn(true)
  }else{
    isExpended = true
    $('#svg-expand').addClass('expanded')
    $('#svg-flowchart').addClass('size')
    expendSVG()
    disableBtn(false)
  }
})
$('#hide-show').on('click', ()=>{ 
  if (isExpended) {
    isExpended = false
    $('#svg-flowchart').removeClass('size')
    collapseSVG();
  }else{
    isExpended = true
    $('#svg-flowchart').addClass('size')
    expendSVG()
  }
})