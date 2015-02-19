$(document).ready(function() {

    d3.select("#image_save").on("click", function(){
      var html = d3.select("svg")
            .attr("version", 1.1)
            .attr("xmlns", "http://www.w3.org/2000/svg")
            .node().parentNode.innerHTML;
      cleanhtml = html.replace(/<\/svg>.*/g,"</svg>")
      console.log(cleanhtml);
      var imgsrc = 'data:image/svg+xml;base64,'+ btoa(cleanhtml);
      var img = '<img src="'+imgsrc+'">'; 
      d3.select("#svgdataurl").html(img);
      console.log(img);
     
     
      var canvas = document.querySelector("canvas"),
    	  context = canvas.getContext("2d");
     
      var image = new Image;
      image.src = imgsrc;
      image.onload = function() {
    	  context.drawImage(image, 0, 0);
     
    	  var canvasdata = canvas.toDataURL("image/png");
     
    	  var pngimg = '<img src="'+canvasdata+'">'; 
      	  d3.select("#pngdataurl").html(pngimg);
          console.log(pngimg);
     
    	  var a = document.createElement("a");
    	  a.download = "sample.png";
    	  a.href = canvasdata;
    	  a.click();
      };
     
    });
});
