#version 120

uniform sampler2D tex0;
uniform float blurSize;
 
void main(void)
{
    vec4 sum = vec4(0.0);
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x - 8.0 * blurSize, gl_TexCoord[0].y)) * 0.0000000;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x - 7.0 * blurSize, gl_TexCoord[0].y)) * 0.0000000;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x - 6.0 * blurSize, gl_TexCoord[0].y)) * 0.0000015;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x - 5.0 * blurSize, gl_TexCoord[0].y)) * 0.0000634;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x - 4.0 * blurSize, gl_TexCoord[0].y)) * 0.0013807;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x - 3.0 * blurSize, gl_TexCoord[0].y)) * 0.0151601;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x - 2.0 * blurSize, gl_TexCoord[0].y)) * 0.0839449;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x - 1.0 * blurSize, gl_TexCoord[0].y)) * 0.2344062;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y))                  * 0.3300863;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x + 1.0 * blurSize, gl_TexCoord[0].y)) * 0.2344062;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x + 2.0 * blurSize, gl_TexCoord[0].y)) * 0.0839449;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x + 3.0 * blurSize, gl_TexCoord[0].y)) * 0.0151601;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x + 4.0 * blurSize, gl_TexCoord[0].y)) * 0.0013807;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x + 5.0 * blurSize, gl_TexCoord[0].y)) * 0.0000634;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x + 6.0 * blurSize, gl_TexCoord[0].y)) * 0.0000015;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x + 7.0 * blurSize, gl_TexCoord[0].y)) * 0.0000000;
    sum += texture2D(tex0, vec2(gl_TexCoord[0].x + 8.0 * blurSize, gl_TexCoord[0].y)) * 0.0000000;
                                                                                         
    gl_FragColor = sum;
}