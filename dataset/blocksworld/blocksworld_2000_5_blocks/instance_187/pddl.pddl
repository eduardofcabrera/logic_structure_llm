

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(on c d)
(on d a)
(ontable e)
(clear b)
(clear c)
)
(:goal
(and
(on c d)
(on d e)
(on e a))
)
)


