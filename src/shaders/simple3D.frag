
varying vec4 v_normal;
varying vec4 v_s;

void main(void)
{
	vec4 normal = normalize(v_normal);
	float lambert = max(dot(normal, normalize(v_s)), 0.0);

	//this is only the intensity value and a full white color
	gl_FragColor = lambert * vec4(1.0, 1.0, 1.0, 1.0);
}