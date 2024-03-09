<template>
	<div v-if="show">
		<div
			tabindex="-1"
			aria-hidden="true"
			class="overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full"
			:class="{ flex: show, hidden: !show }"
		>
			<div class="relative p-4 w-full mx-10 max-h-full">
				<!-- Modal content -->
				<div class="relative bg-white rounded-lg shadow">
					<!-- Modal header -->
					<div
						class="flex items-center justify-between p-4 md:p-5 border-b rounded-t"
					>
						<h3 class="text-lg font-semibold text-gray-900">
							From frame {{ frame.from }} to {{ frame.to }}
						</h3>
						<button
							type="button"
							class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center"
							@click="hideModal"
						>
							<svg
								class="w-3 h-3"
								aria-hidden="true"
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 14 14"
							>
								<path
									stroke="currentColor"
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
								/>
							</svg>
							<span class="sr-only">Close modal</span>
						</button>
					</div>
					<!-- Modal body -->
					<div class="p-4 md:p-5">
						<div class="relative w-full lg:h-full overflow-y-auto">
							<table class="w-full text-sm text-left text-gray-500">
								<thead class="text-sm text-gray-800 uppercase bg-white">
									<tr>
										<th scope="col" class="px-6 py-3 whitespace-nowrap">
											Frame
										</th>
										<th scope="col" class="px-6 py-3 whitespace-nowrap">
											IP Source
										</th>
										<th scope="col" class="px-6 py-3 whitespace-nowrap">
											IP Dest
										</th>
										<th scope="col" class="px-6 py-3 whitespace-nowrap">
											Source Port
										</th>
										<th scope="col" class="px-6 py-3 whitespace-nowrap">
											Dest Port
										</th>
										<th scope="col" class="px-6 py-3 whitespace-nowrap">
											Protocol
										</th>
									</tr>
								</thead>
								<tbody class="border">
									<tr
										v-for="(frame, index) in frame.content"
										:key="index"
										class="border"
									>
										<td class="px-6 py-4 whitespace-nowrap">
											{{ frame.frame }}
										</td>
										<td class="px-6 py-4 whitespace-nowrap font-semibold">
											{{ frame.ip.src }}
										</td>
										<td class="px-6 py-4 whitespace-nowrap font-semibold">
											{{ frame.ip.dst }}
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											{{ frame.port.src }}
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											{{ frame.port.dst }}
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											{{ frame.protocol }}
										</td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="bg-gray-900/50 fixed inset-0 z-40" @click="hideModal"></div>
	</div>
</template>

<script>
export default {
	props: {
		show: {
			type: Boolean,
			required: true,
		},
		frame: {
			type: Object,
			default: () => {},
		},
	},
	methods: {
		hideModal() {
			this.$emit("hide");
		},
	},
};
</script>
