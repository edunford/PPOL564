/**

Macros

**/

/** Spacing  **/
remark.macros.space = function(percentage) {
  return `<div style = "height: ${percentage}%"></div>`;
};

/** Image Orientation  **/

remark.macros.center_img = function(widthpercent) {
  const path = this;
  return `<div style="text-align:center;">
            <img src='${path}' width = ${widthpercent}%/>
          </div>`;
};

/** Text Color  **/
remark.macros.text_color = function(color) {
  const text = this;
  return `<span style="color:${color}">${text}</span>`;
};







