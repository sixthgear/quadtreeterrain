#version 120

uniform sampler2D tex1;
uniform float blurSize;
 
void main(void)
{
    vec4 sum = vec4(0.0);
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 8.0 * blurSize)) * 0.0000000;
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 7.0 * blurSize)) * 0.0000000;
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 6.0 * blurSize)) * 0.0000015;
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 5.0 * blurSize)) * 0.0000634;                                                                                        
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 4.0 * blurSize)) * 0.0013807;
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 3.0 * blurSize)) * 0.0151601;
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 2.0 * blurSize)) * 0.0839449;
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y - 1.0 * blurSize)) * 0.2344062;                                                                                         
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y))                  * 0.3300863;                                                                                         
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 1.0 * blurSize)) * 0.2344062;
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 2.0 * blurSize)) * 0.0839449;
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 3.0 * blurSize)) * 0.0151601;
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 4.0 * blurSize)) * 0.0013807;                                                                                         
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 5.0 * blurSize)) * 0.0000634;
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 6.0 * blurSize)) * 0.0000015;
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 7.0 * blurSize)) * 0.0000000;
    sum += texture2D(tex1, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y + 8.0 * blurSize)) * 0.0000000;
                                                                                         
    gl_FragColor = sum;
}