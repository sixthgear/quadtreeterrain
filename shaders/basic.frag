uniform sampler2D tex0;
 
void main(void)
{
    gl_FragColor = texture2D(tex0, vec2(gl_TexCoord[0].x, gl_TexCoord[0].y));
}