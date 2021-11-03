attribute vec3 a_position;
attribute vec3 a_normal;

attribute vec2 a_uv;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec4 u_eye_position;
uniform vec4 u_light_position;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying vec2 v_uv;
varying float v_light_dist;

void main(void)
{
	vec4 position = vec4(a_position, 1.0);
	vec4 normal = vec4(a_normal, 0.0);

	v_uv = a_uv;
	// local coordinates

	position = u_model_matrix * position;
	v_normal = normalize(u_model_matrix * normal);
	// global coordinates
	v_light_dist = length(u_light_position - position);

	v_s = normalize(u_light_position - position);

	vec4 v = normalize(u_eye_position - position);
	v_h = normalize(v_s + v);


	position = u_view_matrix * position;
	//eye coordinates

	position = u_projection_matrix * position;
	//clip coordinates

	gl_Position = position;
}