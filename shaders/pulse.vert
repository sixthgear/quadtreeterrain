#version 120

uniform float time;

void main() {
	gl_TexCoord[0] = gl_MultiTexCoord0;	
    gl_Position = ftransform();
    gl_Position.x += sin(time * 3 + gl_Position.x) * 0.01;
    gl_Position.y += cos(time * 3 + gl_Position.y ) * 0.01;
}