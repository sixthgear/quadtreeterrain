#version 120

uniform sampler2D tex0;
 
const float threshold_max = 0.7;
const float threshold_min = 0.3;
 
void main(void)
{
    vec4 color = texture2D(tex0, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y));
    float avg = (color.r + color.g + color.b) / 3.0;
    if (avg > threshold_min && avg < threshold_max)
        gl_FragColor = vec4(0.5); // color
    else if (avg > threshold_max)
        gl_FragColor = vec4(0.2); // color
    else
        gl_FragColor = vec4(0.0);
}