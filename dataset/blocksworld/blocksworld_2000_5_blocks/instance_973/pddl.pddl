

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c d)
(ontable d)
(on e a)
(clear b)
(clear c)
(clear e)
)
(:goal
(and
(on c d)
(on d b))
)
)


