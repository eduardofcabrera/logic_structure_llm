

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b c)
(on c a)
(on d e)
(ontable e)
(clear b)
(clear d)
)
(:goal
(and
(on d a)
(on e b))
)
)


