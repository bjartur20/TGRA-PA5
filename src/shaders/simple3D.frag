uniform vec4 u_material_ambient;
uniform vec4 u_material_diffuse;
uniform vec4 u_material_specular;
uniform vec4 u_material_emission;
uniform float u_material_shininess;

uniform vec4 u_light_ambient;
uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;

uniform vec4 u_global_ambient;

uniform sampler2D u_tex_base;
uniform sampler2D u_tex_specular;
uniform sampler2D u_tex_dark_side;
uniform sampler2D u_tex_atmosphere;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying vec2 v_uv;

void main(void)
{
	vec4 specular_mat = u_material_specular * texture2D(u_tex_specular, v_uv) * texture2D(u_tex_atmosphere, v_uv);

	vec4 normal   = normalize(v_normal);
	float lambert = max(dot(normal, normalize(v_s)), 0.0);
	float phong   = max(dot(normal, normalize(v_h)), 0.0);

	vec4 ambient 	= u_light_ambient * u_material_ambient;
	vec4 diffuse 	= u_light_diffuse * u_material_diffuse * lambert
					+ ((1.0 - lambert) / 1.0) * texture2D(u_tex_dark_side, v_uv);  // Add dark side to planets shade
	vec4 specular 	= u_light_specular * specular_mat * pow(phong, u_material_shininess);

	vec4 color = ambient + diffuse + specular
				+ u_global_ambient * u_material_ambient
				+ u_material_emission;

	gl_FragColor = color * (texture2D(u_tex_base, v_uv) + texture2D(u_tex_atmosphere, v_uv));
}