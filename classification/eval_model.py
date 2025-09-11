test_accuracy=model.evaluate(X_test,y_test,verbose=0)
print(test_accuracy[1])
