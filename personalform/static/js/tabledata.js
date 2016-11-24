
var _getData = [];
    $.getJSON("", function(result){
      $.each(result, function(name, value){
        if (name === 'row_list'){
          for(var i = 0; i < value.length; i++){
        _getData.push([]);
          for(var j = 0; j < value[i].length; j++){
              _getData[i].push(value[i][j]);
              }
            }
        }
      })
    });
function updateData(){
  var temp = [];
  for(var i = 0; i < hot1.countRows(); i++){
    if (hot1.getDataAtRow([i]).length != 0) {
      temp.push([]);
      temp[i].push(hot1.getDataAtRow([i]));
    };
  };
  return temp;
};
var
  $$ = function(id) {
      return document.getElementById(id);
  },
  data = _getData,
  //  data = [
  //  ['学号', '姓名', '科研竞赛', '具体加分计算明细', '学科竞赛（20%）','科研情况(10%)', '文体竞赛（5%）', '社会工作', '加分明细（职位）', '能力分', '能力分明细（按照学生手册）'],
  //  ['xx', 'xx', '41.4', '', '美国大学生数学建模竞赛一等奖，50','省级以上期刊排名第一，40', '省级比赛第一名，10', '15', '班级学习委员', '', '一次通过6级，XX分：通过计算机二级，XX分']
  //  ],
  /*        Data传输        */
  container1 = $$('table_1'),
  exampleConsole = $$('console'),
  autosave = $$('autosave'),
  load = $$('load'),
  save = $$('save'),
  searchFiled = $$('prompt'),
  output = $$('output'),
  autosaveNotification,
  hot1;

hot1 = new Handsontable(container1, {
  data: data,
  startRows: 8,
  startCols: 6,
  autoWrapRow: true,
  rowHeaders: true,
  colHeaders: true,
  manualColumnMove: true,
  manualRowMove: true,
  manualColumnResize: true,
  manualRowResize: true,
  contextMenu: true,
  persistentState: true,
  stretchH: 'none',
  search: true,
  /*     多格合并     */
  mergeCells: [
    {}
  ],
  afterChange: function (change, source) {
    if (source === 'loadData') {
      return; //don't save this change
    }
    if (!autosave.checked) {
      return;
    }
    clearTimeout(autosaveNotification);
    $.ajax({
      url: '../json/save.json',
      type: 'GET',
      data: updateData(),
      dataType: 'json',
      async: true,
      success: function (data) {
        //exampleConsole.innerText  = 'Autosaved (' + change.length + ' ' + 'cell' + (change.length > 1 ? 's' : '') + ')';
        autosaveNotification = setTimeout(function() {
          //exampleConsole.innerText ='改动将自动保存';
        }, 1000);
      }
    })
  }
});

Handsontable.Dom.addEvent(save, 'click', function() {
  // save all cell's data
  $.ajax({
    url: '../json/save.json',
    type: 'POST',
    data: updateData(),
    dataType: 'json',
    async: true,
  });
});
Handsontable.Dom.addEvent(output, 'click', function() {
  // save all cell's data
  //alert(updateData())
  //console.log(updateData());
  $.ajax({
      url: "",//传输目标
      type: 'POST',
      data: updateData(),
      //data: getData1,
      dataType: 'json',
      async: true
  })
});
Handsontable.Dom.addEvent(autosave, 'click', function() {
  if (autosave.checked) {

    //exampleConsole.innerText = '改动将自动保存';
  }
  else {
    //exampleConsole.innerText ='改动将不会自动保存';
  }
});
function onlyExactMatch(queryStr, value) {
  return queryStr.toString() === value.toString();
}

Handsontable.Dom.addEvent(searchFiled, 'keyup', function (event) {
    var queryResult = hot1.search.query(this.value);

    console.log(queryResult);
    hot1.render();
});