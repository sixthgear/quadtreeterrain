#version 120

attribute vec2 position;
varying vec2 texcoord;

void main( void )
{
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex; 
    texcoord = gl_Vertex.xy;    
}