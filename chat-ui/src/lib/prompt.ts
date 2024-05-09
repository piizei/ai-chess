// --- Imports ---
import { v4 as uuidv4 } from 'uuid';
// Types

type Variable = {
	key: string;
	value: string;
};

type PromptFragment = {
	id: string;
	name: string;
	content: string;
};

type ComplexPrompt = {
	id: string;
	name: string;
	description: string;
	fragments: PromptFragment[];
	current: boolean;
	variables: Variable[];
};

const createFragment = (name: string, content: string, id?: string): PromptFragment => ({
	id: id || uuidv4(),
	name,
	content
});

const createComplexPrompt = (
	name: string,
	description: string,
	fragments: PromptFragment[] = [],
	current: boolean = false,
	variables: Variable[] = [],
	id?: string
): ComplexPrompt => ({
	id: id || uuidv4(),
	name,
	description,
	fragments,
	current,
	variables
});

const renderPrompt = (prompt: ComplexPrompt): string => {
	return prompt.fragments
		.map((fragment) =>
			prompt.variables.reduce(
				(content, variable) => content.replace(`{${variable.key}}`, variable.value),
				fragment.content
			)
		)
		.join(' ');
};
// Type Guards
function isVariable(object: any): object is Variable {
	return 'key' in object && 'value' in object;
}

function isPromptFragment(object: any): object is PromptFragment {
	return 'id' in object && 'name' in object && 'content' in object;
}

function isComplexPrompt(object: any): object is ComplexPrompt {
	return (
		'id' in object &&
		'name' in object &&
		'fragments' in object &&
		'current' in object &&
		Array.isArray(object.fragments) &&
		object.fragments.every(isPromptFragment)
	);
}

// export everything from this file
export {
	createFragment,
	createComplexPrompt,
	renderPrompt,
	isVariable,
	isPromptFragment,
	isComplexPrompt,
	createExampleData
};
// export types
export type { Variable, PromptFragment, ComplexPrompt };

function createExampleData() {
	const exampleFragments = [];
	for (let i = 0; i < 10; i++) {
		exampleFragments.push(
			createFragment(`Fragment Name ${i}`, `Fragment Content ${i}`, `Fragment Description ${i}`)
		);
	}

	// Example Variables
	const exampleVariables = [
		{ key: 'var1', value: 'Value 1' },
		{ key: 'var2', value: 'Value 2' }
	];

	// Example Complex Prompts
	const exampleComplexPrompts = [];
	for (let i = 0; i < 3; i++) {
		exampleComplexPrompts.push(
			createComplexPrompt(
				`Prompt Name ${i}`,
				`Prompt Description ${i}`,
				exampleFragments.slice(0, 3), // Use the first 3 fragments for each prompt
				i % 2 === 0, // Alternate 'current' flag
				exampleVariables,
				`prompt-is-${i}`
			)
		);
	}
	return exampleComplexPrompts;
}
// Example Fragments
