

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c a)
(ontable d)
(on e d)
(clear b)
(clear c)
(clear e)
)
(:goal
(and
(on c b)
(on d e)
(on e a))
)
)


