#version 120

uniform sampler2D tex0;
 
const float threshold_a = 0.9;
const float threshold_b = 0.6;
const float threshold_c = 0.3;
 
void main(void)
{
    vec4 color = texture2D(tex0, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y));
    float avg = (color.r + color.g + color.b) / 3.0;
    if (avg > threshold_a)    
        gl_FragColor = vec4(0.3,0.0,0.0,0.8); // color
    else if (avg > threshold_b)
        gl_FragColor = vec4(0.8,0.2,0.2,0.8); // color
    else if (avg > threshold_c)
        gl_FragColor = vec4(1.0,0.6,0.6,0.8); // color
    else
        gl_FragColor = vec4(0.1,0.1,0.1,1.0);
}