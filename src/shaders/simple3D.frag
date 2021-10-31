uniform vec4 u_material_diffuse;
uniform vec4 u_material_specular;
uniform float u_material_shininess;

uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;

void main(void)
{
	vec4 normal   = normalize(v_normal);
	float lambert = max(dot(normal, normalize(v_s)), 0.0);
	float phong   = max(dot(v_normal, v_h), 0.0);

	gl_FragColor = u_light_diffuse * u_material_diffuse * lambert
			  + u_light_specular * u_material_specular * pow(phong, u_material_shininess);

	//this is only the intensity value and a full white color
	// gl_FragColor = lambert * vec4(1.0, 1.0, 1.0, 1.0);
}