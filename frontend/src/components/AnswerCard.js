import React from 'react';

const AnswerCard = ({ answer, question, supportingDocuments }) => {
  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-lg p-8 mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          Question: {question}
        </h2>
        
        <div className="bg-white rounded-lg p-6 mb-6 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-700 mb-3">Answer:</h3>
          <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
            {answer}
          </p>
        </div>
        
        {supportingDocuments && supportingDocuments.length > 0 && (
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-700 mb-3">
              📚 Supporting Documents:
            </h3>
            <ul className="list-disc list-inside space-y-2">
              {supportingDocuments.map((doc, index) => (
                <li key={index} className="text-gray-700">
                  {doc}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnswerCard;

