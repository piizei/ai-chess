/**
 * Converts a FormData object to a JSON object.
 * @param formData The FormData object to convert.
 * @returns The resulting JSON object.
 * @example
 * const formData = new FormData();
 * formData.append('name', 'John');
 * formData.append('age', '30');
 * const json = formDataToJson(formData); // { name: 'John', age: '30' }
 * @example
 * const formData = new FormData();
 * formData.append('person[0][name]', 'John');
 * formData.append('person[0][age]', '30');
 * formData.append('person[1][name]', 'Jane');
 * formData.append('person[1][age]', '25');
 * const json = formDataToJson(formData); // { person: [{ name: 'John', age: '30' }, { name: 'Jane', age: '25' }] }
 */

export function formDataToJson(formData: FormData): any {
	const result: any = {};
	for (const [key, value] of formData.entries()) {
		// Check if the key matches the pattern for nested arrays
		const match = key.match(/^(\w+)\[(\d+)\]\[(\w+)\]$/);
		if (match) {
			const [_, arrayName, index, property] = match;
			result[arrayName] = result[arrayName] || [];
			result[arrayName][index] = result[arrayName][index] || {};
			result[arrayName][index][property] = value;
		} else {
			// Convert 'current' to boolean, otherwise assign value directly
			result[key] = key === 'current' ? value === 'on' : value;
		}
	}
	return result;
}
