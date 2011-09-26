#version 120

uniform sampler2D tex0;
uniform float size;
 
void main(void)
{
    vec4 sum = vec4(0.0);
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 4.0 * size)) * 0.0162162162;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 3.0 * size)) * 0.0540540541;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 2.0 * size)) * 0.1216216216;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 1.0 * size)) * 0.1945945946;                                                                                         
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y))              * 0.2270270270;                                                                                         
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 1.0 * size)) * 0.1945945946;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 2.0 * size)) * 0.1216216216;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 3.0 * size)) * 0.0540540541;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 4.0 * size)) * 0.0162162162;                                                                                         
    gl_FragColor = sum;
}

