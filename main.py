


#   try:
#         slither = Slither(solidity_file_path)
#         report = []

#         for contract in slither.contracts:
#             contract_info = {'Contract': contract.name, 'Functions': [], 'Vulnerabilities': []}

#             for function in contract.functions:
#                 function_info = {
#                     'Function': function.name,
#                     'Read': [v.name for v in function.state_variables_read],
#                     'Written': [v.name for v in function.state_variables_written]
#                 }
#                 contract_info['Functions'].append(function_info)
       

#             report.append(contract_info)

#         return jsonify(report)

# except Exception as e:
#         return jsonify({'error': str(e)}), 500
