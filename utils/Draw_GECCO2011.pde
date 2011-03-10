import processing.opengl.*;

String infile = "locs.csv";

int world_x = 1000;
int world_y = 1000;
int radius = 5;
String[] colors = {"#FFFFFF", "#0000FF", "00FF00", "#FFFF00", "#FF0000"};


void setup()
{
  size(world_x, world_y);
  frameRate(1);
  smooth(); 
}

void draw()
{
  stroke(20,20,20,1);
  strokeWeight(3);
  fill(255,255,255,255);
  rect(0,0,world_x,world_y);
  
  String[] lines;
  lines = loadStrings(infile);
 
 stroke(155,155,155);
 strokeWeight(0);
 
 for(int i=0; i < lines.length; i++)
 {
    String[] pieces = split(lines[i], ',');
    float x = Float.valueOf(pieces[3]) * 1000;
    float y = Float.valueOf(pieces[4]) * 1000;
    int type = Integer.parseInt(pieces[5]);
    
    if(type == 0) { fill(255,255,255); }
    else if(type == 1) { fill(0,0,255); }
    else if(type == 2) { fill(0,255,0); }
    else if(type ==3) { fill(255,255,0); }
    else if(type == 4) { fill(255,0,0); }
    else { fill(20,20,20); }    

    ellipse(x, y, radius, radius); 
    
  }
  
  save("cells.png");
  
} // End draw()
