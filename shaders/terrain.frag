#version 120

uniform sampler2D texture;
varying vec2 texcoord;

void main(void)
{
    gl_FragColor = texture2D(texture, texcoord); // vec4(0.5, 0.5, 0.5,1 ); 
}